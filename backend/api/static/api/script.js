// Platforms data passed from Django
const platforms = [
    "Microsoft", "MaddenNFL", "TomClancysRainbowSix", "LeagueOfLegends", 
    "CallOfDuty", "Verizon", "CallOfDutyBlackopsColdWar", "ApexLegends", 
    "Facebook", "WorldOfCraft", "Dota2", "NBA2K", "TomClancysGhostRecon", 
    "Battlefield", "FIFA", "Overwatch", "Xbox(Xseries)", "johnson&johnson", 
    "Amazon", "HomeDepot", "PlayStation5(PS5)", "CS-GO", "Cyberpunk2077", 
    "GrandTheftAuto(GTA)", "Hearthstone", "Nvidia", "Google", "Borderlands", 
    "PlayerUnknownsBattlegrounds(PUBG)", "Fortnite", "RedDeadRedemption(RDR)", 
    "AssassinsCreed"
];

// Function to render dropdown items
document.addEventListener('DOMContentLoaded', () => {
    renderDropdown();
    document.getElementById('form').addEventListener('submit', (event) => {
        event.preventDefault();
        const platform = document.getElementById('dropdownMenuButton').innerText;
        const text = document.getElementById('text').value;
        if (platform === 'Select Platform') {
            alert('Please select a platform');
            return;
        }
        const url = `analyze`;
        fetch(url, {
            method: 'POST',
            body: JSON.stringify({'platform' : platform, 'text': text }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('result').style.display = 'block';
            const sentiment = document.getElementById('sentiment').innerText = data.sentiment;
            if (sentiment === 'Positive') {
                document.getElementById('sentiment').style.color = 'green';
            } else if (sentiment === 'Negative') {
                document.getElementById('sentiment').style.color = 'red';
            } else {
                document.getElementById('sentiment').style.color = 'blue';
            }
        })
    });

    });
function renderDropdown() {
    const dropdownMenu = document.getElementById('dropdownMenu');
    dropdownMenu.innerHTML = ''; // Clear previous items

    // Render all platforms
    platforms.forEach(platform => {
        const item = document.createElement('li');
        item.className = 'dropdown-item';
        item.innerText = platform;
        item.onclick = () => changeDropdownValue(platform);  // Update button text on click
        dropdownMenu.appendChild(item);
    });
}

// Change dropdown button text with the selected platform
function changeDropdownValue(selectedPlatform) {
    const dropdownButton = document.getElementById('dropdownMenuButton');
    dropdownButton.innerText = selectedPlatform; // Set the selected platform as the button text
}


