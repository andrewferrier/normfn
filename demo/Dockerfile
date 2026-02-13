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
RUN mkdir -p /home/demo/documents /home/demo/photos /home/demo/projects && \
    echo "Meeting notes from January 2024" > /home/demo/documents/meeting-notes-01-15-2024.txt && \
    echo "Annual report for 2023" > /home/demo/documents/annual_report_2023.pdf && \
    echo "Project plan" > /home/demo/documents/project-plan.docx && \
    echo "Birthday party photos" > /home/demo/photos/birthday-party-12.25.2023.jpg && \
    echo "Vacation photos" > /home/demo/photos/vacation_pics.jpg && \
    echo "Conference presentation" > /home/demo/photos/conference-2024-02-10.png && \
    echo "README for my project" > /home/demo/projects/README.md && \
    echo "Some code" > /home/demo/projects/main.py && \
    echo "Invoice from March" > /home/demo/invoice-march-2024.pdf && \
    echo "Backup file" > /home/demo/backup-2024-01-01.tar.gz

# Add normfn to PATH in bashrc
RUN echo 'export PATH=/home/demo/normfn:$PATH' >> ~/.bashrc && \
    echo 'export PS1="\u@normfn-demo:\w$ "' >> ~/.bashrc

WORKDIR /home/demo
