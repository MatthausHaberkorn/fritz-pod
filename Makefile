.PHONY: build-base build-rfid create-pod run-rfid all

build-base:
	podman build -f Containerfile.base -t python-poetry-base .

build-rfid:
	podman build -f Containerfile.rfid -t rfid_service .

create-pod:
	if ! podman pod exists fritz_pod ; then podman pod create --name fritz_pod ; fi

run-rfid: create-pod
	podman rm -f rfid_service_container || true
	podman run --privileged --group-add=keep-groups -v /sys:/sys -v /dev:/dev --device /dev/gpiomem --device /dev/mem --device /dev/spidev0.0 --device /dev/spidev0.1 --pod fritz_pod --name rfid_service_container -d rfid_service

all: build-base build-rfid run-rfid