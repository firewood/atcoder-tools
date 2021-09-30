.PHONY: test submit resubmit

test: build
	atcoder-tools test

submit: build
	atcoder-tools submit

resubmit: build
	atcoder-tools submit -u

build: a.out

a.out: main.swift
	swiftc $< -o $@

