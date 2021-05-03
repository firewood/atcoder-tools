#!/bin/sh

rm A/in_?.txt A/out_?.txt
rm B/in_?.txt B/out_?.txt
rm C/in_?.txt C/out_?.txt
rm D/in_?.txt D/out_?.txt
rm E/in_?.txt E/out_?.txt
rm F/in_?.txt F/out_?.txt
atcoder-tools gen --config ./.atcodertools.toml $*
