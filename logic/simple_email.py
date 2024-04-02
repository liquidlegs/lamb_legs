title = data["title"]
name = data["name"]
sub = data["subject_line"]

if title == "Mr":
  data["title"] = "Dr"

if name.lower() == "no name":
  data["name"] = "Rams Bottom"

if sub != None or sub != "":
  split_subject = sub.split(" | ")
  split_impact = split_subject[1].split(" ")
  data["alert_name"] = split_subject[len(split_subject)-1]
  data["impact"] = split_impact[0]
  data["severity"] = split_subject[2]