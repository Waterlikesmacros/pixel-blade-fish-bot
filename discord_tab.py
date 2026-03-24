"""
Enhanced Discord Tab with Loot Selection
Includes panic webhook and individual item selection
"""

import tkinter as tk
from tkinter import ttk, messagebox
from loot_data import LOOT_CATEGORIES, RARITY_ORDER

class EnhancedDiscordTab:
    def __init__(self, parent, settings):
        self.parent = parent
        self.settings = settings
        self.loot_vars = {}
        self.rarity_vars = {}
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the enhanced Discord tab"""
        # Main Discord frame
        discord_frame = tk.Frame(self.parent, bg='#2d2d2d')
        
        # Webhook URL section
        tk.Label(discord_frame, text="Discord Webhook URL:", bg='#2d2d2d', fg='white').pack(anchor='w', padx=10, pady=5)
        
        self.webhook_entry = tk.Text(discord_frame, height=3, bg='#404040', fg='white')
        self.webhook_entry.insert('1.0', self.settings.get('discord_webhook', ''))
        self.webhook_entry.pack(fill='x', padx=10, pady=5)
        
        # Panic webhook section
        panic_frame = tk.LabelFrame(discord_frame, text="Panic Webhook (No Fishing UI Detected)", bg='#2d2d2d', fg='white')
        panic_frame.pack(fill='x', padx=10, pady=10)
        
        self.panic_enabled_var = tk.BooleanVar(value=self.settings.get('panic_webhook_enabled', False))
        tk.Checkbutton(
            panic_frame,
            text="Enable panic webhook when fishing UI not detected",
            variable=self.panic_enabled_var,
            bg='#2d2d2d',
            fg='white',
            selectcolor='#404040'
        ).pack(anchor='w', padx=5, pady=5)
        
        # Loot selection with categories
        loot_frame = tk.LabelFrame(discord_frame, text="Loot Notification Settings", bg='#2d2d2d', fg='white')
        loot_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create scrollable frame for loot items
        canvas = tk.Canvas(loot_frame, bg='#2d2d2d', highlightthickness=0)
        scrollbar = ttk.Scrollbar(loot_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#2d2d2d')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add rarity categories with proper order
        for rarity in RARITY_ORDER:
            self.create_rarity_section(scrollable_frame, rarity)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Send image option
        self.send_image_var = tk.BooleanVar(value=self.settings.get('send_image', True))
        tk.Checkbutton(
            discord_frame,
            text="Send screenshot with loot",
            variable=self.send_image_var,
            bg='#2d2d2d',
            fg='white',
            selectcolor='#404040'
        ).pack(anchor='w', padx=10, pady=10)
        
        return discord_frame
    
    def create_rarity_section(self, parent, rarity):
        """Create a rarity section with category toggle and individual items"""
        rarity_data = LOOT_CATEGORIES[rarity]
        color = rarity_data['color']
        
        # Rarity frame
        rarity_frame = tk.LabelFrame(parent, text=rarity, bg='#2d2d2d', fg=color, font=('Arial', 10, 'bold'))
        rarity_frame.pack(fill='x', padx=5, pady=5)
        
        # Category toggle (selects all items in this rarity)
        self.rarity_vars[rarity] = tk.BooleanVar(value=self.settings.get('send_loot_colors', {}).get(rarity, True))
        rarity_cb = tk.Checkbutton(
            rarity_frame,
            text=f"Select all {rarity}",
            variable=self.rarity_vars[rarity],
            bg='#2d2d2d',
            fg=color,
            selectcolor='#404040',
            font=('Arial', 9, 'bold'),
            command=lambda r=rarity: self.toggle_rarity(r)
        )
        rarity_cb.pack(anchor='w', padx=5, pady=2)
        
        # Individual items frame
        items_frame = tk.Frame(rarity_frame, bg='#2d2d2d')
        items_frame.pack(fill='x', padx=15, pady=2)
        
        self.loot_vars[rarity] = {}
        
        # Add individual item checkboxes
        for item in rarity_data['items']:
            var = tk.BooleanVar(value=self.settings.get('selected_items', {}).get(item, True))
            self.loot_vars[rarity][item] = var
            
            cb = tk.Checkbutton(
                items_frame,
                text=item,
                variable=var,
                bg='#2d2d2d',
                fg=color,
                selectcolor='#404040',
                font=('Arial', 8)
            )
            cb.pack(anchor='w')
    
    def toggle_rarity(self, rarity):
        """Toggle all items in a rarity category"""
        enabled = self.rarity_vars[rarity].get()
        
        # Enable/disable individual item checkboxes
        for item_var in self.loot_vars[rarity].values():
            item_var.set(enabled)
        
        # Update UI appearance
        self.update_rarity_appearance(rarity, enabled)
    
    def update_rarity_appearance(self, rarity, enabled):
        """Update the appearance of rarity section based on selection"""
        # This would update the UI to grey out when disabled
        # Implementation would depend on the specific widgets
        pass
    
    def get_selected_items(self):
        """Get all selected items by rarity"""
        selected = {}
        for rarity, items in self.loot_vars.items():
            selected[rarity] = []
            for item, var in items.items():
                if var.get():
                    selected[rarity].append(item)
        return selected
    
    def get_settings(self):
        """Get current settings from the tab"""
        return {
            'discord_webhook': self.webhook_entry.get('1.0', tk.END).strip(),
            'panic_webhook_enabled': self.panic_enabled_var.get(),
            'send_image': self.send_image_var.get(),
            'send_loot_colors': {rarity: var.get() for rarity, var in self.rarity_vars.items()},
            'selected_items': {
                rarity: {item: var.get() for item, var in items.items()}
                for rarity, items in self.loot_vars.items()
            }
        }
