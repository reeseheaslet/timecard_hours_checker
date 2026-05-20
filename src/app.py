from flask import Flask, render_template, request
from pipeline import run_web_pipeline

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    results_rows = []
    error = None

    pay_period_start = ""
    pay_period_end = ""

    if request.method == "POST":
        executime_file = request.files.get("executime_file")
        firstdue_file = request.files.get("firstdue_file")
        pay_period_start = request.form.get("pay_period_start", "").strip()
        pay_period_end = request.form.get("pay_period_end", "").strip()

        if not executime_file or executime_file.filename == "":
            error = "Please upload an executime CSV."
        elif not firstdue_file or firstdue_file.filename == "":
            error = "Please upload a First Due CSV."
        elif not pay_period_start:
            error = "Please enter a pay period start date."
        elif not pay_period_end:
            error = "Please enter a pay period end date."
        else:
            try:
                # Always include signatures in backend processing.
                result_df = run_web_pipeline(
                    executime_file,
                    firstdue_file,
                    pay_period_start,
                    pay_period_end,
                    include_signatures=True,
                )

                # Always return all review items.
                review_df = result_df[result_df["NeedsReview"]].copy()

                if review_df.empty:
                    results_rows = []
                else:
                    results_rows = review_df.to_dict(orient="records")

            except Exception as e:
                error = f"Error processing files: {e}"

    return render_template(
        "index.html",
        results_rows=results_rows,
        error=error,
        pay_period_start=pay_period_start,
        pay_period_end=pay_period_end,
    )


if __name__ == "__main__":
    app.run(debug=True)