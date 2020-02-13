build-docker:
	docker build . -t capstone_project:1.0
	docker rm -f capstone_project || true
	docker run --cpus 4 --cpu-shares 1024 --name capstone_project -d -v $(PWD):/app:rw \
		-v /Volumes/Marcelo_Sandoval-Castaneda/liene_capstone:/data/liene_capstone:rw \
		capstone_project:1.0
