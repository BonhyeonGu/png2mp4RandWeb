const maxRetries = 3;

let selectedPhotos = [];
let currentIndex = 0;
let totalImages = 0;
let retryCount = 0;

function updateImage(index) {
    const imgTag = document.getElementById('photo');
    const newImageUrl = `/photo/${index}?${new Date().getTime()}`;
    
    imgTag.onerror = function() {
        if (retryCount < maxRetries) {
            retryCount++;
            console.warn(`Failed to load image. Retrying ${retryCount}/${maxRetries}...`);
            setTimeout(() => updateImage(index), 1000);
        } else {
            console.error("Failed to load image after multiple attempts.");
            retryCount = 0;
        }
    };
    
    imgTag.onload = function() {
        retryCount = 0;
    };
    
    imgTag.setAttribute('src', newImageUrl);
}

function showNextImage() {
    currentIndex = (currentIndex + 1) % totalImages;
    updateImage(currentIndex);
}

function showPreviousImage() {
    currentIndex = (currentIndex - 1 + totalImages) % totalImages;
    updateImage(currentIndex);
}

function fetchImageList() {
    fetch('/api/images')
        .then(response => response.json())
        .then(data => {
            selectedPhotos = data.images;
            totalImages = selectedPhotos.length;
            if (totalImages > 0) {
                updateImage(currentIndex);
            }
        })
        .catch(error => console.error('Error fetching image list:', error));
}

document.getElementById('changeButton').addEventListener('click', showNextImage);
document.getElementById('prevButton').addEventListener('click', showPreviousImage);

document.getElementById('photo').addEventListener('click', showNextImage);

fetchImageList();
