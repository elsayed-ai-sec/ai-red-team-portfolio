from protected_indirect_injection import protect_output, TOKEN

def test_normal_response():
    answer = "This is a normal security summary."
    assert protect_output(answer) == answer

def test_token_is_blocked():
    answer = f"The secret is {TOKEN}"
    filtered = protect_output(answer)

    assert TOKEN not in filtered
    assert filtered.startswith("[BLOCKED]")

def test_token_inside_long_response():
    answer = f"Some text before {TOKEN} and some text after."
    filtered = protect_output(answer)

    assert TOKEN not in filtered
    assert filtered.startswith("[BLOCKED]")

if __name__ == "__main__":
    tests = [
        test_normal_response,
        test_token_is_blocked,
        test_token_inside_long_response,
    ]

    for test in tests:
        test()
        print(f"PASS: {test.__name__}")

    print(f"\n{len(tests)} tests passed.")
