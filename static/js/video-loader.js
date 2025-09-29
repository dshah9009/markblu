// Optimized Infinite Scroll with Intersection Observer
class VideoLoader {
    constructor() {
        this.loading = false;
        this.hasMore = true;
        this.currentPage = 1;
        this.videoObserver = null;
        this.init();
    }

    init() {
        this.setupInfiniteScroll();
        this.setupVideoObserver();
        this.observeExistingVideos();
    }

    setupVideoObserver() {
        // Observe videos for lazy loading and auto-play
        this.videoObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                const reel = entry.target;
                const video = reel.querySelector('.reel-video');
                const loader = reel.querySelector('.video-loading');
                const source = video?.querySelector('source');

                if (entry.isIntersecting && video) {
                    // Load video if not loaded
                    if (!video.src && source?.dataset.src) {
                        this.loadVideo(video, source, loader);
                    } else if (video.paused && video.src) {
                        video.play().catch(e => console.log('Play failed:', e));
                    }
                } else if (video?.src) {
                    // Pause when out of view to save resources
                    video.pause();
                }
            });
        }, {
            threshold: 0.5,
            rootMargin: '300px' // Preload videos 300px before visible
        });
    }

    loadVideo(video, source, loader) {
        source.src = source.dataset.src;
        video.src = video.dataset.src;
        video.load();

        video.addEventListener('loadeddata', () => {
            if (loader) loader.style.display = 'none';
            video.play().catch(e => console.log('Auto-play failed:', e));
        }, { once: true });

        // Handle loading errors
        video.addEventListener('error', () => {
            console.error('Video load error');
            if (loader) {
                loader.innerHTML = '<p class="text-white">Failed to load video</p>';
            }
        }, { once: true });
    }

    setupInfiniteScroll() {
        // Create sentinel element at bottom
        const sentinel = document.createElement('div');
        sentinel.id = 'scroll-sentinel';
        sentinel.style.height = '1px';
        document.querySelector('.reel-container')?.appendChild(sentinel);

        const scrollObserver = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting && !this.loading && this.hasMore) {
                this.loadMoreVideos();
            }
        }, {
            rootMargin: '400px' // Start loading 400px before reaching bottom
        });

        scrollObserver.observe(sentinel);
    }

    async loadMoreVideos() {
        if (this.loading || !this.hasMore) return;

        this.loading = true;
        this.showLoadingIndicator();

        try {
            const url = new URL(window.location.href);
            const params = new URLSearchParams(url.search);
            params.set('page', this.currentPage + 1);

            const response = await fetch(`${url.pathname}?${params.toString()}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (!response.ok) throw new Error('Network response failed');

            const data = await response.json();
            
            if (data.videos_html) {
                this.appendVideos(data.videos_html);
                this.currentPage++;
                this.hasMore = data.has_more;
            } else {
                this.hasMore = false;
            }
        } catch (error) {
            console.error('Error loading videos:', error);
            this.showError();
        } finally {
            this.loading = false;
            this.hideLoadingIndicator();
        }
    }

    appendVideos(html) {
        const container = document.querySelector('.reel-container');
        const sentinel = document.getElementById('scroll-sentinel');
        
        // Create temporary container
        const temp = document.createElement('div');
        temp.innerHTML = html;
        
        // Insert before sentinel
        const newReels = temp.querySelectorAll('.reel');
        newReels.forEach(reel => {
            container.insertBefore(reel, sentinel);
            this.videoObserver.observe(reel);
        });

        // Setup mute toggle for new videos
        this.setupMuteToggle(newReels);
    }

    setupMuteToggle(reels) {
        reels.forEach(reel => {
            const video = reel.querySelector('.reel-video');
            if (!video) return;

            video.addEventListener('click', (e) => {
                e.preventDefault();
                const muteIcon = reel.querySelector('.mute-status-icon');
                const icon = muteIcon?.querySelector('.material-icons');
                
                if (video.muted) {
                    video.muted = false;
                    if (icon) icon.textContent = 'volume_up';
                } else {
                    video.muted = true;
                    if (icon) icon.textContent = 'volume_off';
                }
                
                // Show icon briefly
                if (muteIcon) {
                    muteIcon.style.opacity = '1';
                    setTimeout(() => muteIcon.style.opacity = '0', 500);
                }
            });
        });
    }

    observeExistingVideos() {
        document.querySelectorAll('.reel').forEach(reel => {
            this.videoObserver.observe(reel);
        });
        
        // Setup mute for existing videos
        this.setupMuteToggle(document.querySelectorAll('.reel'));
    }

    showLoadingIndicator() {
        const indicator = document.getElementById('loading-indicator');
        if (indicator) indicator.classList.remove('hidden');
    }

    hideLoadingIndicator() {
        const indicator = document.getElementById('loading-indicator');
        if (indicator) indicator.classList.add('hidden');
    }

    showError() {
        const container = document.querySelector('.reel-container');
        const error = document.createElement('div');
        error.className = 'text-center py-4 text-red-500';
        error.textContent = 'Failed to load more videos. Please try again.';
        container?.appendChild(error);
        setTimeout(() => error.remove(), 3000);
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new VideoLoader());
} else {
    new VideoLoader();
}
/Users/deepak/Desktop/deepak/markblu/markblu/static/images/js/video-loader.js