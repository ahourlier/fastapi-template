import argparse
import subprocess

DEFAULT_NUM_REQUESTS = 100
DEFAULT_CONCUR_REQUESTS = 10


def get_args():
    parser = argparse.ArgumentParser(description="Apache Bench Wrapper")

    parser.add_argument(
        "-n",
        type=int,
        help=f"Number of requests sent by Apache Bench (default to {DEFAULT_NUM_REQUESTS})",
    )
    parser.add_argument(
        "-c", type=int, help=f"Concurrence number (default to {DEFAULT_CONCUR_REQUESTS})"
    )
    parser.add_argument(
        "-v",
        action="store_true",
        help="Show complete output of Apache Bench",
    )
    return parser.parse_args()


def request_url(url, num_requests, concur_requests, args):
    text = ""
    command = ["ab", "-n", str(num_requests), "-c", str(concur_requests), url]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output = process.communicate()[0].decode("utf-8")
    if output:
        text += f"\n{url}\n"
        if args.v:
            text = output
            text += "- - - - - - - - - - - - - -"
        else:
            for line in output.split("\n"):
                if (
                    "Complete requests:" in line
                    or "Failed requests:" in line
                    or "Requests per second:" in line
                    or "Time taken for tests:" in line
                ):
                    text += f"    {line}\n"
            text += "\n- - - - - - - - - - - - - -\n"
    print(text)


args = get_args()
num_requests = args.n if args.n else DEFAULT_NUM_REQUESTS
concur_requests = args.c if args.c else DEFAULT_CONCUR_REQUESTS

urls = ["http://127.0.0.1:8000/api/sql_users", "http://127.0.0.1:8000/api/sql_todos?limit=100"]
for url in urls:
    request_url(url, num_requests, concur_requests, args)
