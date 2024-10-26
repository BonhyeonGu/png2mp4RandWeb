let selectedPhotos = [];
let currentIndex = 0;

function fetchImageList() {
    fetch('/api/images')
        .then(response => response.json())
        .then(data => {
            selectedPhotos = data.images;
            if (selectedPhotos.length > 0) {
                updateImage(currentIndex);
            }
        })
        .catch(error => console.error('Error fetching image list:', error));
}

function updateImage(index) {
    const imgTag = document.getElementById('photo');
    const newImageUrl = `${selectedPhotos[index]}?${new Date().getTime()}`;
    imgTag.setAttribute('src', newImageUrl);
}

function showNextImage() {
    currentIndex = (currentIndex + 1) % selectedPhotos.length;
    updateImage(currentIndex);
}

function showPreviousImage() {
    currentIndex = (currentIndex - 1 + selectedPhotos.length) % selectedPhotos.length;
    updateImage(currentIndex);
}

document.getElementById('changeButton').addEventListener('click', showNextImage);
document.getElementById('prevButton').addEventListener('click', showPreviousImage);

document.getElementById('photo').addEventListener('click', showNextImage);

fetchImageList();