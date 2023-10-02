with open(r"_chat.txt", 'r',encoding='utf-8', errors='ignore') as fp:
    text = fp.readlines()
    lines = len(text)
    pollcount =0
    for eachline in text:
        if 'POLL' in eachline:
            pollcount=pollcount+1
    print('Total Number of lines:', lines)
    print('Total polls: '+str(pollcount))

sender_messages = {}

# Iterate through the lines and parse the content
for line in text:
    # Split each line into timestamp, sender, and message
    parts = line.strip().split('] ')
    if len(parts) >= 2:
        timestamp = parts[0][1:]  # Remove the '[' character from the timestamp
        sender_message = parts[1].split(': ', 1)  # Split sender and message

        if len(sender_message) == 2:
            sender = sender_message[0]
            message = sender_message[1]

            # Check if the sender already has a list of messages in the dictionary
            if sender in sender_messages:
                sender_messages[sender].append((timestamp, message))
            else:
                # If not, create a new list with the first message
                sender_messages[sender] = [(timestamp, message)]

# Now you have segregated messages by sender in the sender_messages dictionary
# You can access them as needed
# for sender, messages in sender_messages.items():
#     print(f"Sender: {sender}")
#     for timestamp, message in messages:
#         print(f"Timestamp: {timestamp}")
#         print(f"Message: {message}")
#     print()

# Initialize variables to keep track of the top three senders with the largest messages
top_senders_large_messages = []
top_senders_large_messages_lengths = []

# Iterate through the sender_messages dictionary
for sender, messages in sender_messages.items():
    # Calculate the length of each message sent by this sender
    message_lengths = [len(message) for _, message in messages]

    # Find the largest message length sent by this sender
    largest_message_length = max(message_lengths, default=0)

    # Check if this sender is among the top three with the largest messages
    if len(top_senders_large_messages) < 3 or largest_message_length >= min(top_senders_large_messages_lengths):
        # Add the sender to the top_senders_large_messages list
        top_senders_large_messages.append(sender)
        top_senders_large_messages_lengths.append(largest_message_length)

        # Keep the top_senders_large_messages list sorted by message length
        sorted_indices = sorted(range(len(top_senders_large_messages_lengths)), key=lambda i: top_senders_large_messages_lengths[i], reverse=True)
        top_senders_large_messages = [top_senders_large_messages[i] for i in sorted_indices]
        top_senders_large_messages_lengths = [top_senders_large_messages_lengths[i] for i in sorted_indices]

# Print the top three senders with the largest messages and their message lengths
print("Top Three Senders with Largest Messages:")
for i, sender in enumerate(top_senders_large_messages[:3]):
    print(f"{i+1}. {sender} - {top_senders_large_messages_lengths[i]} characters")


# Initialize variables to keep track of the top three senders
top_senders = []
top_senders_counts = []

# Iterate through the sender_messages dictionary
for sender, messages in sender_messages.items():
    # Calculate the number of messages sent by this sender
    message_count = len(messages)

    # Check if this sender is among the top three senders
    if len(top_senders) < 3 or message_count >= min(top_senders_counts):
        # Add the sender to the top senders list
        top_senders.append(sender)
        top_senders_counts.append(message_count)

        # Keep the top_senders list sorted by message count
        sorted_indices = sorted(range(len(top_senders_counts)), key=lambda i: top_senders_counts[i], reverse=True)
        top_senders = [top_senders[i] for i in sorted_indices]
        top_senders_counts = [top_senders_counts[i] for i in sorted_indices]

# Print the top three senders and their message counts
print("Top Three Senders:")
for i, sender in enumerate(top_senders[:3]):
    print(f"{i+1}. {sender} - {top_senders_counts[i]} messages")

from collections import Counter
import re

# Combine all messages into a single string
all_messages = ' '.join([message for messages in sender_messages.values() for _, message in messages])

# Tokenize the text into words (split by whitespace)
words = re.findall(r'\b\w+\b', all_messages.lower())  # Convert to lowercase for case-insensitivity

# Count the frequency of each word
word_counts = Counter(words)

# Find the most commonly used word
most_common_word, most_common_count = word_counts.most_common(1)[0]

# Print the most commonly used word and its count
print(f"The most commonly used word is: '{most_common_word}'")
print(f"It appears {most_common_count} times.")

# Initialize a dictionary to count messages by date
messages_by_date = {}

# Iterate through the sender_messages dictionary
for sender, messages in sender_messages.items():
    for timestamp, _ in messages:
        # Extract the date from the timestamp
        date_parts = timestamp.split()[0].strip('[]')
        
        # Update the message count for this date
        if date_parts in messages_by_date:
            messages_by_date[date_parts] += 1
        else:
            messages_by_date[date_parts] = 1

# Find the date with the most messages
most_messages_date = max(messages_by_date, key=messages_by_date.get)
most_messages_count = messages_by_date[most_messages_date]

# Print the date with the most messages and its message count
print(f"The date with the most messages is: {most_messages_date}")
print(f"Total messages on that date: {most_messages_count}")

# Create an empty set to store unique senders
unique_senders = set()

# Iterate through the sender_messages dictionary
for sender in sender_messages:
    unique_senders.add(sender)

# Calculate the total number of unique senders
total_senders_count = len(unique_senders)

# Print the total number of people who have sent a message
print(f"Total number of people who have sent a message: {total_senders_count}")

# Initialize a counter for senders with more than 10 messages
senders_with_more_than_10_messages = 0

# Iterate through the sender_messages dictionary
for sender, messages in sender_messages.items():
    # Calculate the number of messages sent by this sender
    message_count = len(messages)
    
    # Check if this sender has sent more than 10 messages
    if message_count > 10:
        senders_with_more_than_10_messages += 1

# Print the total number of people who have sent more than 10 messages
print(f"Total number of people who have sent more than 10 messages: {senders_with_more_than_10_messages}")
active = (senders_with_more_than_10_messages/927)*100
print(f"Which is only {round(active,2)}% of the total group participants")
    