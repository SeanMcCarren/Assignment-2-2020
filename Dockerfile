FROM python:3.6-slim

RUN pip install numpy
RUN pip install matplotlib
RUN pip install seaborn

RUN apt-get update && apt-get install -y curl

RUN curl -sL https://deb.nodesource.com/setup_13.x | bash - && apt-get install -y git nodejs cloc

WORKDIR /usr/jquery-data

COPY prep.py .

COPY jquery_releases.csv .

RUN python prep.py

#RUN rm -rf jquery_releases.csv

# Docker caches results, so if you want to add custom steps to this dockerfile
# (maybe you want to copy in more files) then consider adding these steps below here.
# Otherwise you will need to download all versions of jQuery everytime you add new 
# steps. 

WORKDIR /usr

COPY jsinspect jsinspect

RUN npm install -g ./jsinspect

# Increase the amount of memory nodejs can allocate, this
# prevents JsInspect from running into the GC issues. 
ENV NODE_OPTIONS=--max-old-space-size=4000

WORKDIR /out

RUN echo '[ ! -z "$TERM" -a -r /etc/motd ] && cat /etc/issue && cat /etc/motd' \
    >> /etc/bash.bashrc \
    ; echo "\
===================================================================\n\
= jQuery Code Clone container                                     =\n\
===================================================================\n\
\n\
By Sean McCarren and Maurice Wimmer\n\
\n\
You are currently in /out, where all our scripts and storage resides\n\
From here, run analyse.py to perform the computations. This is a lengthy\n\
computation, hence we store intermediate results. Parallel processing is\n\
used, so more CPUs are beneficial. Additionally, we store the LOC, as\n\
we need this for visualizing later. All storage is done though store.py\n\
\n\
To reset storage, delete results.txt or LOCs.txt\n\
\n\
Visualizing can be done outside the container, in a python notebook.\n\
Using store.py, the computed data can be easily imported \n\
Visualizing can also be done inside the container by running visualize.py. \n\
In that case, store will be used to generate the image in /out \n\
\n\
To start computing, run: python analyse.py [threshold], where threshold is\n\
the JsInspect node threshold that dictates AST similarity\n"\
    > /etc/motd


# Open a bash prompt, such that you can execute commands 
# such as `cloc`. 

ENTRYPOINT ["bash"]