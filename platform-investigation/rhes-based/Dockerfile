FROM centos:7 AS stage1
COPY main.c /
COPY run.sh /
RUN ["/run.sh"]

FROM scratch AS export-stage
COPY --from=stage1 /output32 .
COPY --from=stage1 /output64 .