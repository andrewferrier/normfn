FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    git \
    vim \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m demo
USER demo
WORKDIR /home/demo
ENV HOME=/home/demo

ARG CACHE_BUST
RUN git clone https://github.com/andrewferrier/normfn.git
WORKDIR /home/demo/normfn

# Make normfn executable and add to PATH
RUN chmod +x normfn
ENV PATH="/home/demo/normfn:${PATH}"

# Create demo files and directories with various date formats
RUN mkdir -p /home/demo/documents /home/demo/photos /home/demo/projects /home/demo/downloads && \
    echo "Meeting notes from January 2024" > /home/demo/documents/meeting-notes-01-15-2024.txt && \
    echo "Annual report for 2023" > /home/demo/documents/annual_report_2023.pdf && \
    echo "Project plan" > /home/demo/documents/project-plan.docx && \
    echo "Quarterly report" > "/home/demo/documents/Q1 Report 15 March 2024.docx" && \
    echo "Conference notes" > /home/demo/documents/notes-15.03.2024.txt && \
    echo "Budget spreadsheet" > /home/demo/documents/budget_2024_01_15.xlsx && \
    echo "Contract document" > "/home/demo/documents/contract 25th January 2024.pdf" && \
    echo "Birthday party photos" > /home/demo/photos/birthday-party-12.25.2023.jpg && \
    echo "Vacation photos" > /home/demo/photos/vacation_pics.jpg && \
    echo "Conference presentation" > /home/demo/photos/conference-2024-02-10.png && \
    echo "Screenshot" > "/home/demo/photos/Screenshot 2024-01-20 at 14.30.45.png" && \
    echo "Camera photo" > /home/demo/photos/IMG_20240115_123456.jpg && \
    echo "Video file" > /home/demo/photos/VID_20240115_123456.mp4 && \
    echo "Wedding photo" > "/home/demo/photos/wedding 03 jan 2024.jpg" && \
    echo "README for my project" > /home/demo/projects/README.md && \
    echo "Some code" > /home/demo/projects/main.py && \
    echo "Log file" > /home/demo/projects/debug-log-20240115.txt && \
    echo "Downloaded file" > /home/demo/downloads/report-May-2023.pdf && \
    echo "Invoice" > /home/demo/downloads/invoice_03-04-2024.pdf && \
    echo "Document without date" > /home/demo/downloads/important-document.pdf && \
    echo "Invoice from March" > /home/demo/invoice-march-2024.pdf && \
    echo "Backup file" > /home/demo/backup-2024-01-01.tar.gz && \
    echo "Compressed ISO date" > /home/demo/archive-20240115.zip && \
    echo "Notes file" > /home/demo/notes.txt

# Add normfn to PATH in bashrc
RUN echo 'export PATH=/home/demo/normfn:$PATH' >> ~/.bashrc && \
    echo 'export PS1="\u@normfn-demo:\w$ "' >> ~/.bashrc

WORKDIR /home/demo
