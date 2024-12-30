from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

# Endpoint to fetch stock price
@app.route('/price_snapshot', methods=['GET'])
def price_snapshot():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({"error": "Ticker symbol is required."}), 400
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")["Close"].iloc[-1]
        return jsonify({"ticker": ticker, "price": price})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to fetch financial statements
@app.route('/financials', methods=['GET'])
def financials():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({"error": "Ticker symbol is required."}), 400
    try:
        stock = yf.Ticker(ticker)
        financials = {
            "income_statement": stock.financials.to_dict(),
            "balance_sheet": stock.balance_sheet.to_dict(),
            "cash_flow": stock.cashflow.to_dict()
        }
        return jsonify(financials)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to fetch company info
@app.route('/company_info', methods=['GET'])
def company_info():
    ticker = request.args.get('ticker')
    if not ticker:
        return jsonify({"error": "Ticker symbol is required."}), 400
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return jsonify(info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
