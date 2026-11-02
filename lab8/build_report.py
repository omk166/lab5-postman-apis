from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.section import WD_ORIENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
D=Document();s=D.sections[0]
s.orientation=WD_ORIENT.LANDSCAPE;s.page_width=Inches(11.7);s.page_height=Inches(8.3)
s.top_margin=s.bottom_margin=Inches(.5);s.left_margin=s.right_margin=Inches(.6)
D.styles['Normal'].font.name='Calibri';D.styles['Normal'].font.size=Pt(11)
s.header.paragraphs[0].text='Lab 8 — Docker and containers | Omar Khali | omk166'
s.footer.paragraphs[0].text='Actual Docker Desktop captures • 2 November 2026'
items=[
('Activity 1 — docker ps -a','Lists all containers, including running and stopped containers. The screenshot filters to this lab and formats names, status, and port mappings for readability. Both lab containers are running.','01-docker-ps-a.png'),
('Activity 1 — docker stop','docker stop lab8-users-1 requests that the named container stop. Docker sends its stop signal, waits for the shutdown timeout, then forcefully stops it if needed. The returned container name confirms the stop command completed.','02-docker-stop.png'),
('Activity 1 — docker logs','docker logs lab8-users-1 displays the container’s standard output and error, including Flask startup and request logs. The screenshot uses --tail 5 to keep the last five lines readable. These commands use a container name or ID, rather than an image name.','03-docker-logs.png'),
('Activity 2 — two Docker images','Both images were built successfully: omk166/lab8-omar_khali:0.0.1-RELEASE for Lab 5 on port 5000, and omk166/lab8-omar_khali:0.0.2-RELEASE for GET /get_users on port 3000. Docker tags cannot contain an additional colon; RELEASE is joined with a hyphen.','04-docker-desktop-images.png'),
('Activity 2 — Lab 5 image, port 5000','The first image contains the existing Lab 5 API from omk166/lab5-postman-apis. The app binds to 0.0.0.0 inside the container and publishes port 5000. Its SQLite database persists in a named volume.','06-image-lab5.png'),
('Activity 2 — names API image, port 3000','The second image exposes GET /get_users and queries all names from a SQLite users table. It returns ["Omar", "Ali", "Sara"] from the initial example data. Host 127.0.0.2:3000 avoids an existing service using 127.0.0.1:3000.','05-image-users.png')]
for i,(title,description,picture) in enumerate(items):
 if i:D.add_page_break()
 D.add_heading(title,level=1);D.add_paragraph(description)
 D.add_picture(str(Path('evidence')/picture),width=Inches(9.6))
D.add_page_break();D.add_heading('Verification and reproduction',level=1)
D.add_paragraph(Path('evidence/07-api-verification.txt').read_text())
D.add_paragraph('The isolated database test also passed: GET returns the seeded names, reflects an inserted database row, and rejects POST with HTTP 405.')
D.add_heading('Build and run',level=2)
for line in ['docker compose up --build -d','python verify_live.py','docker ps -a','docker stop lab8-users-1','docker logs lab8-users-1','docker start lab8-users-1']:
 p=D.add_paragraph();r=p.add_run(line);r.font.name='Consolas';r.font.size=Pt(11)
D.add_paragraph('After recording the stop/logs evidence, the users container was restarted. The services remain available at http://127.0.0.1:5000/api/users and http://127.0.0.2:3000/get_users.')
D.add_paragraph('Source: https://github.com/omk166/lab5-postman-apis. Lab 8 code and this report: '+Path('submission.txt').read_text().strip())
D.save('Lab8-Omar-Khali.docx')
print('Saved report with six actual screenshots and verification results.')
