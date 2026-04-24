from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)


def calculate_weekly(estimate: float, save_unit: float, save_count: int, inflow_unit: float) -> dict:
    monthly = estimate / 2
    weekly = monthly / 30 * 7
    weekly_save = save_unit * save_count * 7

    weekly_inflow_budget = weekly - weekly_save
    daily_inflow_budget = weekly_inflow_budget / 7
    daily_inflow_count = math.floor(daily_inflow_budget / inflow_unit) if inflow_unit > 0 else 0

    return {
        "estimate": estimate,
        "monthly": monthly,
        "weekly": weekly,
        "weekly_save": weekly_save,
        "weekly_inflow_budget": weekly_inflow_budget,
        "daily_inflow_budget": daily_inflow_budget,
        "daily_inflow_count": daily_inflow_count,
    }


def calculate_remaining(remaining_days: int, remaining_budget: float, save_unit: float, save_count: int, inflow_unit: float) -> dict:
    remaining_save = save_unit * save_count * remaining_days
    remaining_inflow_budget = remaining_budget - remaining_save
    daily_inflow_budget = remaining_inflow_budget / remaining_days if remaining_days > 0 else 0
    daily_inflow_count = math.floor(daily_inflow_budget / inflow_unit) if inflow_unit > 0 else 0

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
    save_unit = float(data.get("save_unit", 33))
    save_count = int(data.get("save_count", 100))
    inflow_unit = float(data.get("inflow_unit", 27))
    result = calculate_weekly(estimate, save_unit, save_count, inflow_unit)
    return jsonify(result)


@app.route("/api/calculate-remaining", methods=["POST"])
def calculate_remaining_route():
    data = request.get_json()
    remaining_days = int(data.get("remaining_days", 0))
    remaining_budget = float(data.get("remaining_budget", 0))
    save_unit = float(data.get("save_unit", 33))
    save_count = int(data.get("save_count", 100))
    inflow_unit = float(data.get("inflow_unit", 27))
    result = calculate_remaining(remaining_days, remaining_budget, save_unit, save_count, inflow_unit)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
