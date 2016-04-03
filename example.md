---
subject: Hello
author: Maximilian Nöthe
author_email: maximilian.noethe@tu-dortmund.de
# attachments:
#   - /path/to/attachment1
---

{% if recipient.sex == "male" %}Lieber{% else %}Liebe{% endif %} {{ recipient.firstname }},

Wir möchten ein paar Veranstaltungen ankündigen:

* Absolventenfeier
* Sommerakademie

Ein kleines Code-Beispiel:

```
print('Hello World')
```

Mit freundlichen Grüßen
Der PeP et al. Vorstand
