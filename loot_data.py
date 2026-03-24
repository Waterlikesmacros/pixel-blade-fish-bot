"""
Pixel Blade Fishing Bot - Loot Categories and Items
Organized by rarity with proper order: Epic above Rare
"""

LOOT_CATEGORIES = {
    'Vaulted(Red)': {
        'color': '#ff4444',
        'discord_color': 0xFF0000,
        'items': [
            'Abyssal Blade',
            'Void Crown', 
            'Shadow Mantle',
            'Chaos Orb',
            'Eternal Staff'
        ]
    },
    'Legendary(Yellow)': {
        'color': '#ffaa00',
        'discord_color': 0xFFFF00,
        'items': [
            'Golden Sword',
            'Phoenix Feather',
            'Dragon Scale',
            'Thunder Hammer',
            'Crystal Heart'
        ]
    },
    'Epic(Purple)': {
        'color': '#ff44ff',
        'discord_color': 0xFF00FF,
        'items': [
            'Mystic Blade',
            'Enchanted Bow',
            'Magic Shield',
            'Ancient Tome',
            'Spectral Dagger'
        ]
    },
    'Rare(Blue)': {
        'color': '#4444ff',
        'discord_color': 0x0000FF,
        'items': [
            'Steel Sword',
            'Iron Shield',
            'Leather Armor',
            'Health Potion',
            'Mana Crystal'
        ]
    },
    'Common(Grey)': {
        'color': '#888888',
        'discord_color': 0x808080,
        'items': [
            'Wooden Sword',
            'Basic Shield',
            'Cloth Armor',
            'Minor Potion',
            'Small Crystal'
        ]
    }
}

# Rarity order for display
RARITY_ORDER = ['Vaulted(Red)', 'Legendary(Yellow)', 'Epic(Purple)', 'Rare(Blue)', 'Common(Grey)']
