def draftEmail(all_emails):
    body = "hey, here is a summary of all the emails you received today: <br>"
    totalEmailEach = []
    categoriesCount = {}

    for category, emails in all_emails.__dict__.items():
        if isinstance(emails, list):
            total = len(emails)
            totalEmailEach.append((category, total))
            categoriesCount[category] = total  

    if categoriesCount.get("workEmails", 0) == 0:
        workEmailTemplate = "<br><h4 style=\"color: #6060fc;\"><u>Work Emails: 0<u></h4><br><hr>"
        body += workEmailTemplate
    else:
        workEmailTemplate = f"<br><h4 style=\"color: #6060fc;\"><u>Work Emails: {categoriesCount['workEmails']}<u></h4><br>"
        body += workEmailTemplate + "<br>".join(all_emails.workEmails) + "<br><br>"

    if categoriesCount.get("important", 0) == 0:
        importantEmailTemplate = "<br><h4 style=\"color: #6060fc;\"><u>Important/Alerts: 0<u></h4><br><hr>"
        body += importantEmailTemplate
    else:
        importantEmailTemplate = f"<br><h4 style=\"color: #6060fc;\"><u>Important/Alerts: {categoriesCount['important']}<u></h4><br>"
        body += importantEmailTemplate + "<br>".join(all_emails.important) + "<br><br>"

    if categoriesCount.get("personal_Family", 0) == 0:
        personalEmailTemplate = "<br><h4 style=\"color: #6060fc;\"><u>Personal: 0<u></h4><br><hr>"
        body += personalEmailTemplate
    else:
        personalEmailTemplate = f"<br><h4 style=\"color: #6060fc;\"><u>Personal: {categoriesCount['personal_Family']}<u></h4><br>"
        body += personalEmailTemplate + "<br>".join(all_emails.personal_Family) + "<br><br>"

    if categoriesCount.get("newsletters_promotions", 0) == 0:
        newsletterEmailTemplate = "<br><h4 style=\"color: #6060fc;\"><u>Newsletter & Promotions: 0<u></h4><br><hr>"
        body += newsletterEmailTemplate
    else:
        newsletterEmailTemplate = f"<br><h4 style=\"color: #6060fc;\"><u>Newsletter & Promotions: {categoriesCount['newsletters_promotions']}<u></h4><br>"
        body += newsletterEmailTemplate + "<br>".join(all_emails.newsletters_promotions) + "<br><br>"

    if categoriesCount.get("social", 0) == 0:
        socialEmailTemplate = "<br><h4 style=\"color: #6060fc;\"><u>Social: 0<u></h4><br><hr>"
        body += socialEmailTemplate
    else:
        socialEmailTemplate = f"<br><h4 style=\"color: #6060fc;\"><u>Social: {categoriesCount['social']}<u></h4><br>"
        body += socialEmailTemplate + "<br>".join(all_emails.social) + "<br><br>"

    if categoriesCount.get("spam", 0) == 0:
        spamEmailTemplate = "<br><h4 style=\"color: #6060fc;\"><u>Spam: 0<u></h4><br><hr>"
        body += spamEmailTemplate
    else:
        spamEmailTemplate = f"<br><h4 style=\"color: #6060fc;\"><u>Spam: {categoriesCount['spam']}<u></h4><br>"
        body += spamEmailTemplate + "<br>".join(all_emails.spam) + "<br><br>"


    body +="<br><br><p style=\"color: #f7be88;\">Sent from CalmEmail</p>"
    return body
