from caldav_inbox import send_todo
import subprocess
import sys


def main() -> int:
    try:
        process = subprocess.Popen(
            ["zpool", "status", "-x"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )

        output_lines = []
        for line in process.stdout:
            output_lines.append(line)
            sys.stdout.write(line)
            sys.stdout.flush()

        process.wait()

        if process.returncode != 0:
            send_todo(f"zfs status exited with error code: {process.returncode}")
        if output_lines and output_lines[0] != "all pools are healthy\n":
            send_todo("zfs status is unhealthy")
        if not output_lines:
            send_todo("zpool status returned nothing")
        return 0

    except BaseException as e:
        send_todo("zfs status caused python exception")
        raise


if __name__ == "__main__":
    main()