from flask import Flask, render_template, request
from pipeline import run_web_pipeline

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    results_html = None
    error = None

    # Optional: keep form values so they stay in the page after submit
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
                result_df = run_web_pipeline(
                    executime_file,
                    firstdue_file,
                    pay_period_start,
                    pay_period_end,
                )

                # Show mismatches only
                mismatches_df = result_df[result_df["IsMismatch"]]

                if mismatches_df.empty:
                    results_html = "<p>No mismatches found.</p>"
                else:
                    results_html = mismatches_df.to_html(
                        index=False,
                        classes="results-table",
                        border=0,
                    )

            except Exception as e:
                error = f"Error processing files: {e}"

    return render_template(
        "index.html",
        results_html=results_html,
        error=error,
        pay_period_start=pay_period_start,
        pay_period_end=pay_period_end,
    )


if __name__ == "__main__":
    app.run(debug=True)