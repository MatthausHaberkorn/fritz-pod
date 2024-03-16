.PHONY: build-base build-rfid create-pod run-rfid all

build-base:
	podman build -f Containerfile.base -t python-poetry-base .

build-rfid:
	podman build -f Containerfile.rfid -t rfid_service .

build-pod_management:
	podman build -f Containerfile.podmanagement -t pod_management .

create-pod:
	podman pod rm -f fritz_pod || true
	podman pod create --name fritz_pod -p 8000:8000

run-rfid: create-pod
	podman rm -f rfid_service_container || true
	podman run --privileged --group-add=keep-groups -v /sys:/sys -v /dev:/dev --pod fritz_pod --name rfid_service_container --cpu-quota=33000 --cpu-period=100000 -d rfid_service

run-pod_management: create-pod
	podman rm -f pod_management_container || true
	podman run --pod fritz_pod --name pod_management_container -d pod_management

all: build-base build-rfid run-rfid build-pod_management run-pod_management