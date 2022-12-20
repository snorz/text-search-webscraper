FROM httpd:2.4
COPY index.html /usr/local/apache2/htdocs/

RUN sed -i 's/#LoadModule log_forensic_module modules\/mod_log_forensic.so/LoadModule log_forensic_module modules\/mod_log_forensic.so/' /usr/local/apache2/conf/httpd.conf
RUN echo "" >> /usr/local/apache2/conf/httpd.conf
RUN echo "<IfModule log_forensic_module>" >> /usr/local/apache2/conf/httpd.conf
RUN echo "ForensicLog /usr/local/apache2/logs/forensic.log" >> /usr/local/apache2/conf/httpd.conf
RUN echo "</IfModule>" >> /usr/local/apache2/conf/httpd.conf


