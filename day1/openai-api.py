# export OPENAI_API_KEY="..."
# pip3 install openai
# python3 openai-api.py

from openai import OpenAI

client = OpenAI()


def test_openai():
  completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {
          "role": "user",
          "content": "Write a haiku about recursion in programming."
      }
    ]
  )

  print(completion.choices[0].message)

def test_translate_dog():
  completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {
        "role": "user",
        "content": """Translate English to Korean.
Examples:
1. star -> 별
2. cat -> 고양이
3. cup -> 컵
4. code -> 코드
5. history -> 기록"""
      },
      {
        "role": "user",
        "content": "Request: Translate \"dog\"."
      }
    ]
  )

  print(completion.choices[0].message)

def test_movie_review():
  completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {
        "role": "user",
        "content": """Please tell me if the movie review is negative or positive.
Examples:
1. The story was interesting. -> Positive
2. The main character did a great job acting. -> Positive
3. The story was predictable and boring. -> Negative
4. The special effects were great. -> Positive
5. I don't want to see it again. -> Negative
"""
      },
      {
        "role": "user",
        "content": "Request: The storyline was dull and uninspiring."
      }
    ]
  )

  print(completion.choices[0].message)

def test_convert_to_sql():
  completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {
        "role": "user",
        "content": """Convert the following natural language requests into SQL queries.
Examples:
1. "Retrieve all information about employees who earn a salary greater than 50,000.": SELECT * FROM employees WHERE salary > 50000;
2. "Retrieve all details of products that have no stock available.": SELECT * FROM products WHERE stock = 0;
3. "Retrieve the names of students who scored more than 90 in math.": SELECT name FROM students WHERE math_score > 90;
4. "Retrieve all details of orders placed within the last 30 days.": SELECT * FROM orders WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY);
5. "Retrieve a count of customers for each city, grouped by the city they are from.": SELECT city, COUNT(*) FROM customers GROUP BY city;
"""
      },
      {
        "role": "user",
        "content": """Request: Find the average salary of employees in the marketing department.
SQL Query:
"""
      }
    ]
  )

  print(completion.choices[0].message)

def test_chain_of_thought1():
  completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {
        "role": "user",
        "content": """Solve the following problem step-by-step.
Example1: 23 + 47

Step-by-step solution:
1. **Break Down the Numbers**. Identify the tens and ones in each number. For 23, the tens digit is 2 and the ones digit is 3. For 47, the tens digit is 4 and the ones digit is 7.
2. **Add the Ones Place**. Start by adding the digits in the ones place: 3 (from 23) + 7 (from 47) = 10. Since 10 is a two-digit number, write down 0 and carry over 1 to the tens place.
3. **Add the Tens Place**. Next, add the digits in the tens place: 2 (from 23) + 4 (from 47) = 6. Don't forget to add the carried over 1: 6 + 1 = 7.
4. **Combine the Results**. Combine the results from the ones and tens place: The ones place is 0, and the tens place is 7, thus the final sum is 70.

Answer: 70

Example2: 123 - 58

Step-by-step solution:
1. **Understand the Problem:**. Identify the operation you need to perform. In this case, you are asked to subtract 58 from 123.
2. **Break Down the Subtraction:**. Consider subtracting in parts by decomposing the numbers for easier calculation. Subtract 50 first from 123: ( 123 - 50 = 73 )
3. **Complete the Subtraction:**. Finish the subtraction by subtracting the remaining part. Subtract the remaining 8 from 73: ( 73 - 8 = 65 )
4. **Verify the Solution:**. Double-check your calculations to ensure accuracy. Add 58 back to 65 to see if you get 123: ( 65 + 58 = 123 ).

Answer: 65
"""
      },
      {
        "role": "user",
        "content": "Request: 345 + 678 - 123"
      }
    ]
  )

  print(completion.choices[0].message)

def test_chain_of_thought2():
  completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {
        "role": "user",
        "content": """Solve the following logic puzzle step-by-step:
Three friends, Alice, Bob, and Carol, have different favorite colors: red, blue, and green. We know that:
1. Alice does not like red.
2. Bob does not like blue.
3. Carol likes green.

Determine the favorite color of each friend.

Step-by-step solution:
1. **Identify Carol's favorite color:**
- We are told in the problem that Carol likes green. Therefore, Carol's favorite color is green.
2. **Determine colors not liked by Alice and Bob:**
- Alice does not like red, so her favorite color must be either blue or green.
- Bob does not like blue, so his favorite color must be either red or green.
3. **Determine Alice's favorite color:**
- Since Carol's favorite color is green, Alice cannot like green.
- Therefore, Alice's favorite color must be blue.
4. **Determine Bob's favorite color:**
- Alice's favorite color is blue and Carol's favorite color is green.
- The only remaining color for Bob is red.
"""
      },
      {
        "role": "user",
        "content": "Answer:"
      }
    ]
  )

  print(completion.choices[0].message)

def test_chain_of_thought3():
  completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {
        "role": "user",
        "content": """Solve the following logic puzzle step-by-step:
Four people (A, B, C, D) are sitting in a row. We know that:
1. A is not next to B.
2. B is next to C.
3. C is not next to D.

Determine the possible seating arrangements.

Step-by-step solution:
Four people (A, B, C, D) are sitting in a row. We know that:
1. A is not next to B.
2. B is next to C.
3. C is not next to D.
Determine the possible seating arrangements.
**Begin the step-by-step solution:**
1. **Understand the constraints:**
- From the clues, understand that we are arranging A, B, C, D in a row, and specific conditions restrict their placements.
2. **Interpret Clue 2:**
- [B is next to C]: This constraint fixes B and C next to each other. Possible block combinations of B and C are BC and CB.
3. **Analyze placement options within the row for BC and CB:**
- Since BC and CB are blocks, they can occupy positions within the row accordingly. Consider the row as positions 1, 2, 3, and 4 for placement flexibility.
4. **Consider configurations for BC:**
- Possible placements for BC are: BC__, _BC_, __BC.
5. **Consider constraints for each configuration of BC:**
- **BC__:**
- If B occupies position 1 and C position 2, then A and D must fill positions 3 and 4, respectively.
- Clue 1 (A is not next to B): Prevents A sitting in position 2.
- Clue 3 (C is not next to D): Prevents D sitting in position 3.
- Thus, a valid arrangement would be BCAD.
- **_BC_:**
- If B is in position 2 and C in 3, A and D must fill positions 1 and 4.
- Clue 1 prevents A from sitting in position 3.
- Clue 3 prevents D from sitting in position 4.
- Thus, no valid arrangement arises here.
- **__BC:**
- If B occupies position 3 and C occupies position 4, A and D must fill positions 1 and 2.
- Clue 1 prevents A from sitting in position 2.
- Clue 3 prevents D from sitting in position 3.
- Thus, no valid arrangement arises here.
6. **Consider configurations for CB:**
- Possible placements for CB are: CB__, _CB_, __CB.
7. **Consider constraints for each configuration of CB:**
- **CB__:**
- If C occupies position 1 and B occupies position 2, then A and D must be in positions 3 and 4.
- Clue 1 prevents A sitting at position 2.
- Clue 3 prevents D from sitting at position 1.
- Thus, a valid arrangement would be CABD.
- **_CB_:**
- If C is in position 2 and B in 3, A and D must fill positions 1 and 4.
- Clue 1 prevents A from being next to B.
- Clue 3 prevents D from being next to C.
- Thus, no valid arrangement arises here.
- **__CB:**
- If C occupies position 3 and B occupies position 4, A and D must be in positions 1 and 2.
- Clue 1 prevents A from sitting in position 4.
- Clue 3 prevents D from sitting in position 3.
- Thus, no valid arrangement arises here.
8. **Verify arrangements:**
- Validate each arrangement carefully against all constraints, ensuring none are violated.
...
        """
      },
      {
        "role": "user",
        "content": "Answer:"
      }
    ]
  )

  print(completion.choices[0].message)

test_openai()
test_translate_dog()
test_movie_review()
test_convert_to_sql()
test_chain_of_thought1()
test_chain_of_thought2()
test_chain_of_thought3()
