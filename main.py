import subprocess

def run_tests():
    result = subprocess.run(['pytest', 'tests'], capture_output=True, text=True)

    #You can use the -v (verbose) option with pytest to get more detailed information about which tests are running.
    # result = subprocess.run(['pytest', 'tests', '-v'], capture_output=True, text=True)

    # you can run tests in parallel by specifying the -n option followed by the number of parallel processes
    # result = subprocess.run(['pytest', 'tests', '-v', '-n', '4'], capture_output=True, text=True)

    print(result.stdout)
    print(result.stderr)

if __name__ == "__main__":
    run_tests()
