'''
#feed.html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>MarkBlu Reels</title>
  <script src="https://cdn.tailwindcss.com?plugins=forms"></script>
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" />
  <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet" />
  <style>
    body {
      font-family: 'Roboto', sans-serif;
      background: #000;
      color: #fff;
      margin: 0;
    }
    .reel-container {
      height: 100vh;
      overflow-y: scroll;
      scroll-snap-type: y mandatory;
      -webkit-overflow-scrolling: touch;
    }
    .reel {
      height: 100vh;
      scroll-snap-align: start;
      position: relative;
      display: flex;
      align-items: flex-end;
      justify-content: center;
    }
    .reel video {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      object-fit: contain;
      background-color: #000;
      z-index: 0;
      cursor: pointer;
    }
    .top-left-info {
      position: absolute;
      top: 1rem;
      left: 1rem;
      z-index: 10;
      font-size: 0.85rem;
      color: white;
      line-height: 1.5;
    }
    .reel-content {
      position: relative;
      z-index: 2;
      width: 100%;
      padding: 1rem;
      background: linear-gradient(to top, rgba(0, 0, 0, 0.85), transparent);
    }
    .actions-sidebar {
      position: absolute;
      right: 1rem;
      bottom: 6rem;
      z-index: 10;
      display: flex;
      flex-direction: column;
      gap: 1.2rem;
      align-items: center;
    }
    .action-item {
      font-size: 0.75rem;
      text-align: center;
      color: white;
    }
    .action-item .material-icons {
      font-size: 2rem;
      margin-bottom: 4px;
    }
    .message {
      padding: 1rem;
      text-align: center;
      background: #1f2937;
      color: #d1d5db;
    }
  </style>
</head>
<body>

{% if no_results %}
  <p class="message">No exact matches found. Showing similar properties:</p>
{% endif %}

<div class="reel-container">
  {% for video in videos %}
  <div class="reel">
    <!-- 🎥 Video with click-to-mute -->
    <video autoplay loop playsinline onclick="this.muted = !this.muted">
      <source src="{{ video.video.url }}" type="video/mp4" />
      Your browser does not support the video tag.
    </video>

    <!-- 📍 Top Left Info -->
    <div class="top-left-info">
      <div><span class="material-icons text-sm">location_on</span> {{ video.city }}</div>
      <div><span class="material-icons text-sm transform scale-y-[-1]">trending_flat</span> {{ video.area }}</div>
      <div><span class="material-icons text-sm transform scale-y-[-1]">trending_flat</span> ₹{{ video.price_min }} - ₹{{ video.price_max }} Lakh</div>
      <div><span class="material-icons text-sm transform scale-y-[-1]">trending_flat</span> {{ video.property_type }}</div>
      <div><span class="material-icons text-sm transform scale-y-[-1]">trending_flat</span> {{ video.properties }}</div>
    </div>

    <!-- 📦 Bottom Info -->
    <div class="reel-content text-sm">
      <div class="mb-2">
        <span class="bg-green-500 text-white px-2 py-1 rounded text-xs">RERA Approved</span>
        <span class="bg-gray-700 text-white px-2 py-1 rounded text-xs ml-2">Token: ₹{{ video.token_amount }}</span>
      </div>
      <p><strong>Broker:</strong> {{ video.agent.user.first_name }} {{ video.agent.user.last_name }}</p>
      <p><strong>Project:</strong> {{ video.agent.project_location }}</p>
      <p>Market Price: ₹{{ video.market_price_per_sqft }}/sqft</p>
      <p>Size: {{ video.property_size_sqft }} sqft</p>
    </div>

    <!-- 🔘 Sidebar Actions -->
    <div class="actions-sidebar">
      <div class="action-item"
        onclick="{% if user.is_authenticated %}window.location.href='tel:{{ video.agent.mobile }}'{% else %}window.location.href='{% url 'user-login' %}?next={{ request.get_full_path|urlencode }}'{% endif %}">
        <span class="material-icons">call</span> Call Broker
      </div>
      <div class="action-item"><span class="material-icons">event</span> Schedule</div>
      <div class="action-item"><span class="material-icons">bookmark_border</span> Save</div>
      <div class="action-item"><span class="material-icons">location_on</span> Location</div>
    </div>

  </div>
  {% endfor %}
</div>

</body>
</html>
'''