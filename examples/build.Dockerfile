FROM debian:latest AS build-stage
# This image can be changed. The build stage must be "build-stage" for a PBS shell.
# Build steps go here

FROM scratch AS export-stage
COPY --from=build-stage /path/to/file .

