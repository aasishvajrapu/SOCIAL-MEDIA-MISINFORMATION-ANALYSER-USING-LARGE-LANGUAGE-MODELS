from analyzer import analyze_content

text = input("Enter social media text: ")

label, explanation = analyze_content(text)

print("\nResult:")
print("Classification:", label)
print("Explanation:", explanation)
