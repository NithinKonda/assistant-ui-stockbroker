from flask import Flask, jsonify, request, Response, stream_with_context
import yfinance as yf
from flask_cors import CORS
import json
import time

app = Flask(__name__)

# Configure CORS to allow all necessary endpoints
CORS(app, 
     resources={
         r"/*": {
             "origins": ["http://localhost:3000"],
             "methods": ["GET", "POST", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "expose_headers": ["Content-Type", "Transfer-Encoding"],
             "supports_credentials": True,
             "max_age": 3600
         }
     })

# Financial data helper functions
def get_income_statement(ticker: str, period: str = "annual", limit: int = 5):
    try:
        stock = yf.Ticker(ticker)
        financials = stock.financials
        if period == "annual":
            return financials.iloc[:, :limit].to_json()
        else:
            return financials.T.iloc[-limit:].to_json()
    except Exception as e:
        return {"error": f"Error fetching income statement: {str(e)}"}

def get_balance_sheet(ticker: str, period: str = "annual", limit: int = 5):
    try:
        stock = yf.Ticker(ticker)
        balance_sheet = stock.balance_sheet
        if period == "annual":
            return balance_sheet.iloc[:, :limit].to_json()
        else:
            return balance_sheet.T.iloc[-limit:].to_json()
    except Exception as e:
        return {"error": f"Error fetching balance sheet: {str(e)}"}

def get_cash_flow(ticker: str, period: str = "annual", limit: int = 5):
    try:
        stock = yf.Ticker(ticker)
        cash_flow = stock.cashflow
        if period == "annual":
            return cash_flow.iloc[:, :limit].to_json()
        else:
            return cash_flow.T.iloc[-limit:].to_json()
    except Exception as e:
        return {"error": f"Error fetching cash flow statement: {str(e)}"}

def get_stock_price(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        return {
            "ticker": ticker,
            "price": stock.info.get("currentPrice"),
            "currency": stock.info.get("currency"),
        }
    except Exception as e:
        return {"error": f"Error fetching stock price: {str(e)}"}

# Streaming helper function
def generate_stream():
    """Generate streaming response data"""
    messages = [
        {"type": "start", "message": "Starting process..."},
        {"type": "progress", "message": "Processing..."},
        {"type": "complete", "message": "Complete!"}
    ]
    
    for message in messages:
        yield f"data: {json.dumps(message)}\n\n"
        time.sleep(0.5)  # Simulate processing time

# Financial data endpoints
@app.route('/income-statement', methods=['GET', 'OPTIONS'])
def income_statement():
    if request.method == 'OPTIONS':
        response = jsonify({"message": "Preflight request successful"})
        response.status_code = 200
        return response
        
    ticker = request.args.get('ticker')
    period = request.args.get('period', 'annual')
    limit = int(request.args.get('limit', 5))
    return jsonify(get_income_statement(ticker, period, limit))

@app.route('/balance-sheet', methods=['GET', 'OPTIONS'])
def balance_sheet():
    if request.method == 'OPTIONS':
        response = jsonify({"message": "Preflight request successful"})
        response.status_code = 200
        return response
        
    ticker = request.args.get('ticker')
    period = request.args.get('period', 'annual')
    limit = int(request.args.get('limit', 5))
    return jsonify(get_balance_sheet(ticker, period, limit))

@app.route('/cash-flow', methods=['GET', 'OPTIONS'])
def cash_flow():
    if request.method == 'OPTIONS':
        response = jsonify({"message": "Preflight request successful"})
        response.status_code = 200
        return response
        
    ticker = request.args.get('ticker')
    period = request.args.get('period', 'annual')
    limit = int(request.args.get('limit', 5))
    return jsonify(get_cash_flow(ticker, period, limit))

@app.route('/stock-price', methods=['GET', 'OPTIONS'])
def stock_price():
    if request.method == 'OPTIONS':
        response = jsonify({"message": "Preflight request successful"})
        response.status_code = 200
        return response
        
    ticker = request.args.get('ticker')
    return jsonify(get_stock_price(ticker))

# Thread and streaming endpoints
@app.route('/threads', methods=['POST', 'OPTIONS'])
@app.route('/api/threads', methods=['POST', 'OPTIONS'])
def create_thread():
    if request.method == 'OPTIONS':
        response = jsonify({"message": "Preflight request successful"})
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.status_code = 200
        return response
        
    thread_id = "example-thread-id"
    return jsonify({"thread_id": thread_id, "status": "created"}), 200

@app.route('/threads/<thread_id>/runs/stream', methods=['POST', 'OPTIONS'])
def stream_runs(thread_id):
    print(f"Received stream request for thread ID: {thread_id}")  # Debug log
    if request.method == 'OPTIONS':
        response = jsonify({"message": "Preflight request successful"})
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.status_code = 200
        return response

    def stream():
        for data in generate_stream():
            print(f"Streaming data: {data}")  # Debug log
            yield data

    response = Response(
        stream_with_context(stream()),
        mimetype='text/event-stream'
    )
    response.headers['Content-Type'] = 'text/event-stream'
    response.headers['Cache-Control'] = 'no-cache'
    response.headers['Connection'] = 'keep-alive'
    return response


@app.route('/threads/<thread_id>/state', methods=['GET', 'OPTIONS'])
@app.route('/api/threads/<thread_id>/state', methods=['GET', 'OPTIONS'])
def get_thread_state(thread_id):
    if request.method == 'OPTIONS':
        response = jsonify({"message": "Preflight request successful"})
        response.status_code = 200
        return response
    
    data = {"thread_id": thread_id, "state": {}}
    return jsonify(data), 200

# Run configuration
if __name__ == "__main__":
    # Enable debug mode for development
    app.run(debug=True, port=5000)