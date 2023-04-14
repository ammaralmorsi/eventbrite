curl -X 'POST' \
  'http://127.0.0.1:8000/categories/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Music",
  "sub_categories": [
    "DJ/Dance",
    "Rock",
    "Latin",
    "Classical",
    "Hip Hop/Rap",
    "EDM/Electronic",
    "Jazz",
    "World",
    "Blues & Jazz",
    "R&B",
    "Country",
    "Acoustic",
    "Pop",
    "Top40",
    "Singer/Songwriter",
    "Electronic",
    "Indie",
    "Blues",
    "Reggae",
    "Americana",
    "Folk",
    "Alternative",
    "Cultural",
    "Metal",
    "Religious/Spiritual",
    "Bluegrass",
    "Experimental",
    "Pyschadelic"
  ]
}'

curl -X 'POST' \
  'http://127.0.0.1:8000/categories/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Performing & Visual Arts",
  "sub_categories": [
    "Comedy",
    "Dance",
    "Theatre",
    "Fine Art",
    "Painting",
    "Crafts",
    "Musical",
    "Literary Arts",
    "Ballet",
    "sculpture",
    "Design",
    "Opera"
  ]
}'

curl -X 'POST' \
  'http://127.0.0.1:8000/categories/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Holiday",
  "sub_categories": [
    "Christmas",
    "Halloween/Haunt",
    "Independence Day",
    "New Year'\''s Eve",
    "Thanksgiving"
  ]
}'
curl -X 'POST' \
  'http://127.0.0.1:8000/categories/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Health",
  "sub_categories": [
    "Mental Health",
    "Spa",
    "Yoga",
    "Medical"
  ]
}'

curl -X 'POST' \
  'http://127.0.0.1:8000/categories/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Hobbies",
  "sub_categories": [
    "Drawing & Painting",
    "DIY",
    "Books",
    "Gaming",
    "Photography",
    "Adult",
    "Anim/Comics"
  ]
}'


curl -X 'POST' \
  'http://127.0.0.1:8000/categories/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Business",
  "sub_categories": [
    "Career",
    "Education",
    "Startups & Small Business",
    "Real Estate",
    "Sales & Marketing",
    "Environment & Sustainability",
    "Finance",
    "Investment",
    "Design",
    "Non Profit & NGOs",
    "Media"
  ]
}'
curl -X 'POST' \
  'http://127.0.0.1:8000/categories/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Food & Drink",
  "sub_categories": [
    "Food",
    "Beer",
    "Wine",
    "Spirits"
  ]
}'

curl -X 'POST' \
  'http://127.0.0.1:8000/categories/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Sports & Fitness",
  "sub_categories": [
    "Football",
    "Basketball",
    "Tennis",
    "Exercise",
    "Cycling",
    "Soccer",
    "Running",
    "Golf",
    "Walking",
    "Fighting & Martial Arts",
    "Swimming & Water Sports",
    "Wrestling",
    "Baseball",
    "Mountain Biking",
    "Camps"
  ]
}'
