import json
import os
import random
import requests
from pathlib import Path

from flask import Flask, render_template, request, session
from dotenv import load_dotenv

# Import existing live price function directly
from utils.api_handler import fetch_live_price, get_prices_for_symbols


load_dotenv(override=True)

app = Flask(__name__)
app.config["SECRET_KEY"] = "cryptoguard-demo-key"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_FALLBACK_MODEL = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-2.5-flash-lite")

WALLET_OWNER = "Abdul Rehman"
WALLET_PIN = "1122"
DATA_DIR = Path(__file__).parent / "data"
WALLET_FILE = DATA_DIR / "wallet_abdul_rehman.json"


def ensure_wallet_file() -> None:
    """Create wallet file with defaults if it does not exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not WALLET_FILE.exists():
        default_wallet = {
            "owner": WALLET_OWNER,
            "usdt_balance": 1000.0,
            "holdings": [],
        }
        WALLET_FILE.write_text(json.dumps(default_wallet, indent=2), encoding="utf-8")


def load_wallet() -> dict:
    """Load wallet data from local JSON file."""
    ensure_wallet_file()
    with WALLET_FILE.open("r", encoding="utf-8") as file:
        wallet = json.load(file)

    wallet.setdefault("owner", WALLET_OWNER)
    wallet.setdefault("usdt_balance", 0.0)
    wallet.setdefault("holdings", [])
    return wallet


def save_wallet(wallet: dict) -> None:
    """Persist wallet data to local JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    WALLET_FILE.write_text(json.dumps(wallet, indent=2), encoding="utf-8")


def upsert_holding(wallet: dict, symbol: str, amount: float) -> None:
    """Add or update a holding in wallet."""
    symbol = symbol.upper()
    for row in wallet["holdings"]:
        if row.get("symbol") == symbol:
            row["amount"] = amount
            return
    wallet["holdings"].append({"symbol": symbol, "amount": amount})

RANDOM_DASHBOARD_SYMBOLS = [
    "BTC",
    "ETH",
    "SOL",
    "XRP",
    "ADA",
    "DOGE",
    "BNB",
    "AVAX",
    "DOT",
    "MATIC",
]


def get_dashboard_market_data() -> list[dict]:
    """Fetch live prices for a random set of coins for the dashboard."""
    selected = random.sample(RANDOM_DASHBOARD_SYMBOLS, k=6)
    prices = get_prices_for_symbols(selected)

    rows: list[dict] = []
    for symbol in selected:
        details = prices.get(symbol, {})
        if not details.get("success"):
            continue
        rows.append(
            {
                "symbol": symbol,
                "price_usd": details.get("price_usd"),
                "change_24h": details.get("change_24h"),
                "market_cap": details.get("market_cap"),
                "volume_24h": details.get("volume_24h"),
            }
        )

    # Sort by market cap (largest first) for a more professional dashboard order.
    rows.sort(key=lambda row: row.get("market_cap") or 0, reverse=True)
    return rows


def get_wallet_live_snapshot(wallet: dict) -> dict:
    """Return holdings with live valuation and portfolio totals."""
    holdings = wallet.get("holdings", [])
    symbols = [row.get("symbol", "").upper() for row in holdings if row.get("symbol")]
    prices = get_prices_for_symbols(symbols) if symbols else {}

    live_rows: list[dict] = []
    total_usd = 0.0

    for row in holdings:
        symbol = row.get("symbol", "").upper()
        amount = float(row.get("amount", 0.0) or 0.0)
        details = prices.get(symbol, {})
        price = float(details.get("price_usd", 0.0) or 0.0)
        value = amount * price
        total_usd += value
        live_rows.append(
            {
                "symbol": symbol,
                "amount": amount,
                "price_usd": price,
                "value_usd": value,
                "change_24h": details.get("change_24h"),
            }
        )

    return {
        "owner": wallet.get("owner", WALLET_OWNER),
        "usdt_balance": float(wallet.get("usdt_balance", 0.0) or 0.0),
        "holdings": live_rows,
        "holdings_value_usd": total_usd,
        "total_wallet_usd": total_usd + float(wallet.get("usdt_balance", 0.0) or 0.0),
    }


def market_action(change_24h: float | None) -> dict:
    """Simple market action classifier for coin signals."""
    if change_24h is None:
        return {"action": "HOLD", "tone": "neutral", "reason": "No trend data"}
    if change_24h <= -5:
        return {"action": "BUY", "tone": "positive", "reason": "Strong dip detected"}
    if change_24h >= 7:
        return {"action": "SELL", "tone": "warning", "reason": "Short-term spike"}
    return {"action": "HOLD", "tone": "neutral", "reason": "Stable trend"}


def build_market_signals(rows: list[dict]) -> list[dict]:
    """Attach BUY/SELL/HOLD action to live market rows."""
    signals: list[dict] = []
    for row in rows:
        signal = market_action(row.get("change_24h"))
        signals.append({**row, **signal})
    return signals


def get_next_buy_recommendation(usdt_balance: float, held_symbols: set[str], signals: list[dict]) -> dict:
    """Recommend next coin to buy using USDT balance + live trend."""
    if usdt_balance < 20:
        return {
            "coin": None,
            "message": "USDT balance is low. Add more balance before new buying.",
            "tone": "warning",
        }

    buy_candidates = [row for row in signals if row.get("action") == "BUY" and row.get("symbol") not in held_symbols]
    if not buy_candidates:
        return {
            "coin": None,
            "message": "No strong BUY setup right now. Better to hold and watch market.",
            "tone": "neutral",
        }

    pick = sorted(buy_candidates, key=lambda row: row.get("change_24h") or 0)[0]
    allocation = round(usdt_balance * 0.25, 2)
    return {
        "coin": pick.get("symbol"),
        "message": f"Consider buying {pick.get('symbol')} with about ${allocation} USDT in phased entries (DCA).",
        "tone": "positive",
    }


def build_chatbot_context(wallet: dict) -> str:
    """Build context string about user wallet and market for chatbot prompts."""
    snapshot = get_wallet_live_snapshot(wallet)
    market_rows = get_dashboard_market_data()

    context = f"""You are a friendly and knowledgeable crypto investment advisor. Current user portfolio:

Portfolio Owner: {snapshot['owner']}
USDT Balance: ${snapshot['usdt_balance']:,.2f}
Total Holdings Value: ${snapshot['holdings_value_usd']:,.2f}
Total Wallet Value: ${snapshot['total_wallet_usd']:,.2f}

Current Holdings:
"""
    if snapshot["holdings"]:
        for row in snapshot["holdings"]:
            context += f"  • {row['symbol']}: {row['amount']:.4f} coins @ ${row['price_usd']:,.4f} (24h: {row['change_24h']:+.2f}%) = ${row['value_usd']:,.2f}\n"
    else:
        context += "  • No coins held yet (ready to invest)\n"

    context += f"\nLive Market Snapshot (Top 6 Coins):\n"
    for row in market_rows[:6]:
        context += f"  • {row['symbol']}: ${row['price_usd']:,.4f} (24h: {row['change_24h']:+.2f}%)\n"

    context += "\nAnswer questions about crypto, portfolio management, and investment suggestions in a friendly, conversational tone. Keep responses concise (2-3 sentences). Do not provide financial advice, only educational guidance."

    return context


def chatbot_reply(user_message: str, wallet: dict) -> str:
    """Get AI response using Gemini API with wallet context."""
    if not GEMINI_API_KEY:
        return "⚠️ Gemini API key not configured. Please add GEMINI_API_KEY to your .env file."

    context = build_chatbot_context(wallet)
    model_candidates = []
    for model_name in [GEMINI_MODEL, GEMINI_FALLBACK_MODEL]:
        if model_name and model_name not in model_candidates:
            model_candidates.append(model_name)

    last_error_message = None

    for model_name in model_candidates:
        endpoint = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model_name}:generateContent?key={GEMINI_API_KEY}"
        )

        try:
            response = requests.post(
                endpoint,
                headers={"Content-Type": "application/json"},
                json={
                    "systemInstruction": {
                        "parts": [{"text": context}],
                    },
                    "contents": [
                        {
                            "role": "user",
                            "parts": [{"text": user_message}],
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 250,
                    },
                },
                timeout=20,
            )
            response.raise_for_status()
            data = response.json()

            candidates = data.get("candidates", [])
            if candidates:
                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                texts = [part.get("text", "") for part in parts if part.get("text")]
                if texts:
                    reply = "".join(texts).strip()
                    if model_name != GEMINI_MODEL:
                        reply += f"\n\n(used fallback model: {model_name})"
                    return reply

            last_error_message = "⚠️ Unexpected response format from Gemini."

        except requests.exceptions.Timeout:
            last_error_message = "⏱️ Request timed out. Please try again."
            continue
        except requests.exceptions.HTTPError as e:
            resp_text = ""
            try:
                resp_text = e.response.text
            except Exception:
                resp_text = str(e)

            if e.response is not None and e.response.status_code in {400, 404, 429, 503}:
                last_error_message = f"Gemini model '{model_name}' failed: {resp_text}"
                continue

            if e.response is not None and e.response.status_code == 401:
                return "🔐 Invalid Gemini API key. Please check GEMINI_API_KEY in your .env."

            return f"❌ Gemini Error ({e.response.status_code}): {resp_text}"
        except requests.exceptions.RequestException as e:
            last_error_message = f"⚠️ Network error: {e}"
            continue
        except Exception as e:
            return f"⚠️ Chatbot error: {str(e)}"

    if last_error_message:
        return (
            "⚠️ Gemini is unavailable right now. "
            f"Tried models: {', '.join(model_candidates)}.\n"
            f"Last error: {last_error_message}"
        )

    return "⚠️ Gemini did not return a usable response."



def get_investment_suggestion(change_24h: float | None, market_cap: float | None) -> dict:
    """Return a beginner-friendly suggestion based on simple heuristics.

    This is educational guidance, not financial advice.
    """
    if change_24h is None:
        return {
            "decision": "RESEARCH FIRST",
            "reason": "24h trend data is unavailable. Check chart history and fundamentals before investing.",
            "tone": "neutral",
        }

    large_cap = (market_cap or 0) >= 1_000_000_000

    if change_24h <= -5 and large_cap:
        return {
            "decision": "CONSIDER INVESTING (DCA)",
            "reason": "Price dipped significantly in 24h on a large-cap asset. Consider phased buying instead of one-time entry.",
            "tone": "positive",
        }

    if change_24h >= 8:
        return {
            "decision": "WAIT / AVOID FOMO",
            "reason": "Strong short-term spike detected. Wait for stabilization before entry.",
            "tone": "warning",
        }

    return {
        "decision": "HOLD / WATCH",
        "reason": "No strong signal from 24h move. Monitor trend, market cap, and project fundamentals.",
        "tone": "neutral",
    }


@app.route("/", methods=["GET", "POST"])
def index():
    """Render form and show live price + investment suggestion on submit."""
    coin_query = ""
    result = None
    suggestion = None
    dashboard_rows = get_dashboard_market_data()

    if request.method == "POST":
        # Read user input from form
        coin_query = request.form.get("coin", "").strip()

        if coin_query:
            # Keep original price-fetching logic by calling existing utility
            result = fetch_live_price(coin_query)
            if result.get("success"):
                suggestion = get_investment_suggestion(result.get("change_24h"), result.get("market_cap"))
        else:
            result = {"success": False, "error": "Please enter a coin name or symbol."}

    return render_template(
        "index.html",
        coin_query=coin_query,
        result=result,
        suggestion=suggestion,
        dashboard_rows=dashboard_rows,
    )


@app.route("/wallet", methods=["GET", "POST"])
def wallet():
    """PIN-protected wallet page for Abdul Rehman."""
    wallet = load_wallet()
    message = None
    message_tone = "neutral"

    if request.method == "POST":
        action = request.form.get("action", "")
        pin = request.form.get("pin", "").strip()

        if pin != WALLET_PIN:
            message = "Invalid PIN. Use 1122 to update wallet."
            message_tone = "warning"
        else:
            if action == "set_usdt":
                try:
                    wallet["usdt_balance"] = max(0.0, float(request.form.get("usdt_balance", "0")))
                    save_wallet(wallet)
                    message = "USDT balance updated successfully."
                    message_tone = "positive"
                except ValueError:
                    message = "Please enter a valid USDT balance."
                    message_tone = "warning"
            elif action == "upsert_coin":
                symbol = request.form.get("symbol", "").strip().upper()
                try:
                    amount = max(0.0, float(request.form.get("amount", "0")))
                except ValueError:
                    amount = -1.0

                if not symbol or amount < 0:
                    message = "Enter valid coin symbol and amount."
                    message_tone = "warning"
                else:
                    upsert_holding(wallet, symbol, amount)
                    save_wallet(wallet)
                    message = f"Wallet updated: {symbol} balance saved."
                    message_tone = "positive"

    snapshot = get_wallet_live_snapshot(load_wallet())
    return render_template(
        "wallet.html",
        owner=WALLET_OWNER,
        pin_hint="1122",
        wallet=snapshot,
        message=message,
        message_tone=message_tone,
    )


@app.route("/suggestion", methods=["GET"])
def suggestion_page():
    """Suggestion page: next coin to buy + hold/sell table from live market."""
    wallet = load_wallet()
    snapshot = get_wallet_live_snapshot(wallet)
    dashboard_rows = get_dashboard_market_data()
    signals = build_market_signals(dashboard_rows)
    held_symbols = {row.get("symbol") for row in snapshot.get("holdings", [])}
    next_buy = get_next_buy_recommendation(snapshot.get("usdt_balance", 0.0), held_symbols, signals)

    holding_actions: list[dict] = []
    for row in snapshot.get("holdings", []):
        signal = market_action(row.get("change_24h"))
        holding_actions.append({**row, **signal})

    return render_template(
        "suggestion.html",
        owner=WALLET_OWNER,
        wallet=snapshot,
        next_buy=next_buy,
        market_signals=signals,
        holding_actions=holding_actions,
    )


@app.route("/chat", methods=["GET", "POST"])
def chat_page():
    """AI-powered chatbot that understands wallet, prices, and suggestions."""
    wallet = load_wallet()
    snapshot = get_wallet_live_snapshot(wallet)

    provider_signature = f"gemini:{GEMINI_MODEL}"
    if session.get("chat_provider") != provider_signature:
        session.pop("chat_history", None)
        session["chat_provider"] = provider_signature
        session.modified = True

    messages = session.get("chat_history", [])
    bot_response = None

    if request.method == "POST":
        user_input = request.form.get("message", "").strip()
        
        if user_input:
            # Add user message to history
            messages.append({"role": "user", "content": user_input})
            
            # Get AI response
            bot_response = chatbot_reply(user_input, wallet)
            messages.append({"role": "assistant", "content": bot_response})
            
            # Save chat history in session (limit to last 20 messages)
            if len(messages) > 40:  # 20 user-bot pairs
                messages = messages[-40:]
            session["chat_history"] = messages
            session["chat_provider"] = provider_signature
            session.modified = True

    return render_template(
        "chat.html",
        owner=WALLET_OWNER,
        wallet=snapshot,
        messages=messages,
        bot_response=bot_response,
    )


@app.route("/clear-chat", methods=["POST"])
def clear_chat():
    """Clear chat history."""
    session.pop("chat_history", None)
    session.pop("chat_provider", None)
    session.modified = True
    return {"status": "success", "message": "Chat history cleared"}


@app.route("/chat-config", methods=["GET"])
def chat_config():
    """Debug route showing current chat API configuration (does not expose keys)."""
    return {
        "gemini_model": GEMINI_MODEL,
        "gemini_fallback_model": GEMINI_FALLBACK_MODEL,
        "gemini_key_present": bool(GEMINI_API_KEY),
    }


if __name__ == "__main__":
    # Run a local development server. Use python app.py to launch.
    app.run(host="127.0.0.1", port=5000, debug=True)
