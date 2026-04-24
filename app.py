from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

SAVE_COST_PER_DAY = 100 * 33       # 3,300원 (100건 * 33원)
INFLOW_COST_PER_UNIT = 27           # 27원/건


def calculate_weekly(estimate: float) -> dict:
    monthly = estimate / 2
    weekly = monthly / 30 * 7
    weekly_save = SAVE_COST_PER_DAY * 7

    weekly_inflow_budget = weekly - weekly_save
    daily_inflow_budget = weekly_inflow_budget / 7
    daily_inflow_count = math.floor(daily_inflow_budget / INFLOW_COST_PER_UNIT)

    return {
        "estimate": estimate,
        "monthly": monthly,
        "weekly": weekly,
        "weekly_save": weekly_save,
        "weekly_inflow_budget": weekly_inflow_budget,
        "daily_inflow_budget": daily_inflow_budget,
        "daily_inflow_count": daily_inflow_count,
    }


def calculate_remaining(remaining_days: int, remaining_budget: float) -> dict:
    remaining_save = SAVE_COST_PER_DAY * remaining_days
    remaining_inflow_budget = remaining_budget - remaining_save
    daily_inflow_budget = remaining_inflow_budget / remaining_days if remaining_days > 0 else 0
    daily_inflow_count = math.floor(daily_inflow_budget / INFLOW_COST_PER_UNIT)

    return {
        "remaining_days": remaining_days,
        "remaining_budget": remaining_budget,
        "remaining_save": remaining_save,
        "remaining_inflow_budget": remaining_inflow_budget,
        "daily_inflow_budget": daily_inflow_budget,
        "daily_inflow_count": daily_inflow_count,
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    estimate = float(data.get("estimate", 0))
    result = calculate_weekly(estimate)
    return jsonify(result)


@app.route("/api/calculate-remaining", methods=["POST"])
def calculate_remaining_route():
    data = request.get_json()
    remaining_days = int(data.get("remaining_days", 0))
    remaining_budget = float(data.get("remaining_budget", 0))
    result = calculate_remaining(remaining_days, remaining_budget)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
