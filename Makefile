.PHONY: build-base build-rfid create-pod run-rfid all

build-base:
	podman build -f Containerfile.base -t python-poetry-base .

build-rfid:
	podman build -f Containerfile.rfid -t rfid_service .

create-pod:
	podman pod rm -f fritz_pod || true
	podman pod create --name fritz_pod

run-rfid: create-pod
	podman rm -f rfid_service_container || true
	podman run --privileged --group-add=keep-groups -v /sys:/sys -v /dev:/dev --pod fritz_pod --name rfid_service_container --cpu-quota=33000 --cpu-period=100000 -d rfid_service

all: build-base build-rfid run-rfid