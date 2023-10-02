from collections import Counter
import re

with open(r"_chat.txt", 'r',encoding='utf-8', errors='ignore') as fp:
    text = fp.readlines()
    lines = len(text)
    pollcount =0
    for eachline in text:
        if 'POLL' in eachline:
            pollcount=pollcount+1
    print('Total Number of lines:', lines)
    print('Total polls: '+str(pollcount))

#To find the top three people with largest text message

sender_messages = {}
for line in text:
    parts = line.strip().split('] ')
    if len(parts) >= 2:
        timestamp = parts[0][1:]
        sender_message = parts[1].split(': ', 1)
        if len(sender_message) == 2:
            sender = sender_message[0]
            message = sender_message[1]
            if sender in sender_messages:
                sender_messages[sender].append((timestamp, message))
            else:
                sender_messages[sender] = [(timestamp, message)]
top_senders_large_messages = []
top_senders_large_messages_lengths = []

for sender, messages in sender_messages.items():
    message_lengths = [len(message) for _, message in messages]

    largest_message_length = max(message_lengths, default=0)
    if len(top_senders_large_messages) < 3 or largest_message_length >= min(top_senders_large_messages_lengths):
        top_senders_large_messages.append(sender)
        top_senders_large_messages_lengths.append(largest_message_length)
        sorted_indices = sorted(range(len(top_senders_large_messages_lengths)), key=lambda i: top_senders_large_messages_lengths[i], reverse=True)
        top_senders_large_messages = [top_senders_large_messages[i] for i in sorted_indices]
        top_senders_large_messages_lengths = [top_senders_large_messages_lengths[i] for i in sorted_indices]

print("\nTop Three Senders with Largest Messages:\n")
for i, sender in enumerate(top_senders_large_messages[:3]):
    print(f"{i+1}. {sender} \t-\t {top_senders_large_messages_lengths[i]} characters")


#THe top three most active users (aka people with most number of messages)
top_senders = []
top_senders_counts = []
for sender, messages in sender_messages.items():
    message_count = len(messages)
    if len(top_senders) < 3 or message_count >= min(top_senders_counts):
        top_senders.append(sender)
        top_senders_counts.append(message_count)
        sorted_indices = sorted(range(len(top_senders_counts)), key=lambda i: top_senders_counts[i], reverse=True)
        top_senders = [top_senders[i] for i in sorted_indices]
        top_senders_counts = [top_senders_counts[i] for i in sorted_indices]

print("\nTop Three Senders:\n")
for i, sender in enumerate(top_senders[:3]):
    print(f"{i+1}. {sender} \t- \t{top_senders_counts[i]} messages")


# Top ten most common words used in the group
all_messages = ' '.join([message for messages in sender_messages.values() for _, message in messages])

words = re.findall(r'\b\w+\b', all_messages.lower())
word_counts = Counter(words)
top_five_words = word_counts.most_common(10)

print("\nTop ten most common words used in the group!\n")
for word, count in top_five_words:
    print(f"{word}:\t {count} times")

# The day with the most number of messages in the group (Aka the day on which our group was most active)
messages_by_date = {}

for sender, messages in sender_messages.items():
    for timestamp, _ in messages:
        date_parts = timestamp.split()[0].strip('[]')
        if date_parts in messages_by_date:
            messages_by_date[date_parts] += 1
        else:
            messages_by_date[date_parts] = 1
most_messages_date = max(messages_by_date, key=messages_by_date.get)
most_messages_count = messages_by_date[most_messages_date]

print(f"\nThe date with the most messages is:\t {most_messages_date}")
print(f"Total messages on that date:\t {most_messages_count}")

# Some analytics on our active users
unique_senders = set()

for sender in sender_messages:
    unique_senders.add(sender)
total_senders_count = len(unique_senders)

print(f"\nTotal number of people who have sent a message:\t {total_senders_count}")
senders_with_more_than_10_messages = 0
for sender, messages in sender_messages.items():
    message_count = len(messages)
    if message_count > 10:
        senders_with_more_than_10_messages += 1
print(f"\nTotal number of people who have sent more than 10 messages:\t {senders_with_more_than_10_messages}")
active = (senders_with_more_than_10_messages/927)*100
print(f"Which is only {round(active,2)}% of the total group participants")
    
#For debugging purposes

# for sender, messages in sender_messages.items():
#     print(f"Sender: {sender}")
#     for timestamp, message in messages:
#         print(f"Timestamp: {timestamp}")
#         print(f"Message: {message}")
#     print()