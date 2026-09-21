from flask import Flask, request, render_template_string
import bcrypt

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Hasher</title>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            font-family: Arial, sans-serif;
            background: #f4f4f4;
        }

        .box {
            width: 100%;
            max-width: 500px;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 5px 25px rgba(0,0,0,.1);
        }

        h1 {
            text-align: center;
            margin-top: 0;
        }

        input, textarea, button {
            width: 100%;
            font-size: 16px;
        }

        input {
            padding: 13px;
            border: 1px solid #ccc;
            border-radius: 6px;
            margin-bottom: 12px;
        }

        textarea {
            height: 110px;
            padding: 12px;
            border: 1px solid #ccc;
            border-radius: 6px;
            resize: none;
            margin-top: 10px;
        }

        button {
            padding: 13px;
            border: none;
            border-radius: 6px;
            background: #222;
            color: white;
            cursor: pointer;
            margin-bottom: 10px;
        }

        button:hover {
            background: #444;
        }

        .message {
            text-align: center;
            margin-top: 10px;
        }
    </style>
</head>

<body>

<div class="box">

    <h1>Password Hasher</h1>

    <form method="POST">
        <input
            type="password"
            name="password"
            placeholder="Enter password"
            required
        >

        <button type="submit">
            Generate Hash
        </button>
    </form>

    {% if hashed %}
        <textarea id="hash" readonly>{{ hashed }}</textarea>

        <button onclick="copyHash()">
            Copy Hash
        </button>

        <p id="message" class="message"></p>
    {% endif %}

</div>

<script>
function copyHash() {
    const hash = document.getElementById("hash");

    navigator.clipboard.writeText(hash.value)
        .then(() => {
            document.getElementById("message").textContent =
                "Hash copied!";
        })
        .catch(() => {
            hash.select();
            document.execCommand("copy");
            document.getElementById("message").textContent =
                "Hash copied!";
        });
}
</script>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    hashed = None

    if request.method == "POST":
        password = request.form.get("password", "")

        if password:
            hashed = bcrypt.hashpw(
                password.encode("utf-8"),
                bcrypt.gensalt(rounds=12)
            ).decode("utf-8")

    return render_template_string(HTML, hashed=hashed)


if __name__ == "__main__":
    app.run(debug=True)
