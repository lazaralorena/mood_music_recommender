document.addEventListener('DOMContentLoaded', () => {
    const moodButtons = document.querySelectorAll('.mood-btn');
    const musicRecommendation = document.getElementById('music-recommendation');
    const songTitle = document.getElementById('song-title');
    const artistName = document.getElementById('artist-name');
    const musicLink = document.getElementById('music-link');
    const anotherSongBtn = document.getElementById('another-song');
    const favoriteBtn = document.getElementById('favorite-btn');
    const favoritesList = document.getElementById('favorites-list');
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;

    let currentMood = '';
    let currentSongId = null;

    // Add common styles to all mood buttons
    moodButtons.forEach(button => {
        button.classList.add('p-4', 'rounded-lg', 'text-white', 'font-bold', 'text-lg', 'transition-colors', 'duration-200');
    });

    // Function to fetch music recommendation
    const getMusicRecommendation = async (mood) => {
        try {
            const response = await fetch(`/api/music/${mood}`, {
                headers: {
                    'X-CSRF-TOKEN': csrfToken
                }
            });
            
            if (!response.ok) {
                if (response.status === 401) {
                    window.location.href = '/login';
                    return;
                }
                throw new Error('No music found for this mood');
            }
            
            const data = await response.json();
            currentSongId = data.id;
            
            // Update the UI with the recommendation
            songTitle.textContent = data.title;
            artistName.textContent = `by ${data.artist}`;
            musicLink.href = data.url;
            musicRecommendation.classList.remove('hidden');
            
            // Update favorite button state
            updateFavoriteButtonState();
        } catch (error) {
            alert('Sorry, could not find music for this mood. Please try again.');
        }
    };

    // Function to toggle favorite status
    const toggleFavorite = async () => {
        if (!currentSongId) return;

        try {
            const method = favoriteBtn.classList.contains('favorited') ? 'DELETE' : 'POST';
            const response = await fetch(`/api/favorite/${currentSongId}`, {
                method: method,
                headers: {
                    'X-CSRF-TOKEN': csrfToken
                }
            });

            if (!response.ok) {
                if (response.status === 401) {
                    window.location.href = '/login';
                    return;
                }
                throw new Error('Failed to update favorite status');
            }

            updateFavoriteButtonState();
            loadFavorites();
        } catch (error) {
            alert('Failed to update favorite status. Please try again.');
        }
    };

    // Function to check if current song is favorited
    const updateFavoriteButtonState = async () => {
        if (!currentSongId || !favoriteBtn) return;

        try {
            const response = await fetch('/api/favorites', {
                headers: {
                    'X-CSRF-TOKEN': csrfToken
                }
            });
            const favorites = await response.json();
            
            const isFavorited = favorites.some(fav => fav.id === currentSongId);
            favoriteBtn.classList.toggle('favorited', isFavorited);
            favoriteBtn.classList.toggle('bg-rose-400', !isFavorited);
            favoriteBtn.classList.toggle('bg-rose-600', isFavorited);
            favoriteBtn.textContent = isFavorited ? '♥ Remove from Favorites' : '♥ Add to Favorites';
        } catch (error) {
            console.error('Failed to check favorite status:', error);
        }
    };

    // Function to load and display favorites
    const loadFavorites = async () => {
        if (!favoritesList) return;

        try {
            const response = await fetch('/api/favorites', {
                headers: {
                    'X-CSRF-TOKEN': csrfToken
                }
            });
            
            if (!response.ok) {
                if (response.status === 401) {
                    window.location.href = '/login';
                    return;
                }
                throw new Error('Failed to load favorites');
            }

            const favorites = await response.json();
            favoritesList.innerHTML = favorites.length ? '' : '<p class="text-gray-600 text-center">No favorites yet</p>';

            favorites.forEach(fav => {
                const favElement = document.createElement('div');
                favElement.className = 'bg-white/60 backdrop-blur-sm rounded-lg p-4';
                favElement.innerHTML = `
                    <div class="flex justify-between items-center">
                        <div>
                            <h3 class="font-medium text-gray-800">${fav.title}</h3>
                            <p class="text-gray-600">by ${fav.artist}</p>
                            <p class="text-sm text-gray-500">Mood: ${fav.mood}</p>
                        </div>
                        <a href="${fav.url}" target="_blank" 
                           class="px-4 py-2 bg-teal-400 hover:bg-teal-500 text-white rounded transition-colors duration-300">
                            Listen
                        </a>
                    </div>
                `;
                favoritesList.appendChild(favElement);
            });
        } catch (error) {
            console.error('Failed to load favorites:', error);
        }
    };

    // Event listeners for mood buttons
    moodButtons.forEach(button => {
        button.addEventListener('click', () => {
            currentMood = button.dataset.mood;
            getMusicRecommendation(currentMood);
        });
    });

    // Event listener for "Get Another Song" button
    if (anotherSongBtn) {
        anotherSongBtn.addEventListener('click', () => {
            if (currentMood) {
                getMusicRecommendation(currentMood);
            }
        });
    }

    // Event listener for favorite button
    if (favoriteBtn) {
        favoriteBtn.addEventListener('click', toggleFavorite);
    }

    // Load favorites on page load
    loadFavorites();
}); 