mkbin:
	mkdir -p bin

build: mkbin
	$(CXX) -Wall -o ./bin/brainf src/*.c

run: build
	./bin/brainf ./test/test.bf

clean:
	rm -rf bin
