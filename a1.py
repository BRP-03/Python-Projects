from plyer import notification
import time

# नोटिफिकेशन दिखाने के लिए plyer का notify() फंक्शन
def show_simple_notification():
    title = 'Simple Notification'
    message = 'This is a test notification from plyer library.'
    
    # notify() फंक्शन को कॉल करें
    notification.notify(
        title=title,
        message=message,
        app_name='Python Notification App',  # नोटिफिकेशन सेंटर में ऐप का नाम
        timeout=10  # नोटिफिकेशन 10 सेकंड बाद अपने आप बंद हो जाएगा
    )
    print("Notification has been sent.")

# एक और उदाहरण: एक टाइमर नोटिफिकेशन
def show_timer_notification():
    title = 'Timer Notification'
    message = 'Your 5-second timer has ended!'
    
    print("Starting a 5-second timer...")
    time.sleep(5) # 5 सेकंड के लिए प्रोग्राम को रोकें
    
    # टाइमर खत्म होने पर नोटिफिकेशन दिखाएं
    notification.notify(
        title=title,
        message=message,
        app_name='Python Timer',
        timeout=5
    )
    print("Timer has ended and notification has been sent.")

# दोनों उदाहरणों को चलाएं
if __name__ == "__main__":
    show_simple_notification()
    time.sleep(12)  # पहले नोटिफिकेशन के बंद होने का इंतज़ार करें
    show_timer_notification()