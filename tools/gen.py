#!/usr/bin/env python3
import json, io

import argparse
ap = argparse.ArgumentParser(description='Build the Cogwork Manual HTML app from the processed payload + wiki data.')
ap.add_argument('--payload', default='data/payload.json')
ap.add_argument('--wiki', default='data/wiki.json')
ap.add_argument('--out', default='docs/cogwork-manual.html')
args = ap.parse_args()

payload = open(args.payload).read()
wiki_payload = open(args.wiki).read()

MODS = [
 ("create","Create","⛭","#c9a227","The foundation. Rotational power, contraptions, trains — the kinetic language every other mod here speaks."),
 ("createaddition","Crafts & Additions","⚡","#e0c04a","Bridges Create rotation to Forge Energy. Alternators make FE from rotation; electric motors turn it back."),
 ("bits_n_bobs","Bits 'n' Bobs","⌗","#c9a227","Small mechanical parts and quality-of-life blocks that fill the gaps in base Create."),
 ("copycats","Copycats+","⧉","#9a978c","Copycat blocks in far more shapes. Wear any block's texture on any shape."),
 ("createframed","Framed Blocks","▧","#8f7f5f","Another take on copycats — framed panels, slopes and shapes that borrow any texture."),
 ("createcasing","Extended Casings","▩","#b5673a","Casing variants in every wood and metal, plus matching shafts and belts."),
 ("dndecor","Design 'n' Decor","▦","#b5673a","Industrial decoration in Create's exact art style. The biggest building-block set in the pack."),
 ("dndesires","Dreams & Desires","⟠","#8f7fa8","New machines, materials and an eerie branch of Create tech. Adds seething, sanding and hydraulic compacting."),
 ("create_factory","Create: Factory","⌸","#8f9fb8","Factory logistics — packagers, stock networks and on-demand crafting chains."),
 ("create_connected","Create: Connected","◈","#5a9c88","Quality-of-life additions and connectivity blocks for larger builds."),
 ("createdieselgenerators","Diesel Generators","⛽","#7f6a4a","Oil, refining and combustion engines. A whole fuel chain feeding huge stress output."),
 ("petrochem","Petrochem","⚗","#5a9c88","Petrochemical processing — crude oil, distillation and plastics."),
 ("create_new_age","Create: New Age","⌘","#5a9c88","Advanced and nuclear power generation feeding Create's kinetic network."),
 ("electroenergetics","Electroenergetics","⚡","#e0c04a","Electrical machinery, wiring and power distribution on top of Create."),
 ("powergrid","Powergrid","⌁","#8f9fb8","Power transmission infrastructure — poles, lines and grid management."),
 ("createtransmission","Transmission","✇","#5a9c88","Extra ways to move rotation around: gearboxes, drives and couplings."),
 ("gnkinetics","GN Kinetics","⛭","#c9a227","More kinetic blocks and alternative power sources."),
 ("gearbox","Gearbox","⊞","#9a978c","Additional gearing and rotation-routing components."),
 ("create_enchantment_industry","Enchantment Industry","⚗","#5a9c88","Automate enchanting. Liquid experience, disenchanting, printing books, industrial XP."),
 ("createfood","Create Food","⌸","#7fa05a","An enormous food expansion built on Create processing. The largest item set in the pack."),
 ("creategarnished","Garnished","⎔","#7fa05a","Food, farming and new machines. Peanuts, cheese and a lot of processing recipes."),
 ("createcafe","Create Café","☕","#b5673a","Coffee, drinks and café culture, automated end to end."),
 ("create_confectionery","Confectionery","⌾","#e0a0b0","Sweets, candy and sugar processing through mixing and pressing chains."),
 ("createmechanicalconfection","Mechanical Confection","◍","#e0a0b0","More confectionery machinery and chocolate processing."),
 ("create_chocolate_fountain","Chocolate Fountain","◉","#8f6a4a","Exactly what it says. A working chocolate fountain."),
 ("create_winery","Winery","⌛","#8f5f7a","Grapes, fermentation and ageing. Wine as a multi-stage process."),
 ("create_integrated_farming","Integrated Farming","❦","#7fa05a","Farming automation that plugs directly into Create's kinetics."),
 ("mechanical_botany","Mechanical Botany","✿","#7fa05a","Insolators and composters — plant processing at industrial scale."),
 ("farmersdelight","Farmer's Delight","⌸","#7fa05a","Cooking, cutting boards and hearty food. Many Create chains feed into it."),
 ("create_sa","Stuff & Additions","⚒","#b5673a","Tools, armour and gadgets in Create's style, including better backtanks."),
 ("someassemblyrequired","Some Assembly Required","⌬","#c9a227","Assembly-line tooling and extra sequenced crafting options."),
 ("create_things_and_misc","Things & Misc","◇","#9a978c","A grab-bag of extra items, blocks and small machines."),
 ("createmetalwork","Metalwork","▬","#9a978c","Metal processing, alloys and smithing built onto Create."),
 ("create_train_parts","Train Parts","⛓","#9a978c","Extra rolling stock, carriages and train fittings."),
 ("createrailwaysnavigator","Railways Navigator","⌖","#8f9fb8","Train timetables, route planning and station navigation."),
 ("bellsandwhistles","Bells & Whistles","♪","#c9a227","Station decoration, signage, bogie steps and railway atmosphere."),
 ("create_hypertube","Hypertube","◯","#5a9c88","High-speed tube transport for players and items."),
 ("cmpackagecouriers","Package Couriers","▤","#8f9fb8","Couriers and drones that deliver Create's packages for you."),
 ("create_mobile_packages","Mobile Packages","▣","#8f9fb8","Package handling on the move."),
 ("create_wrapped","Wrapped","▥","#8f9fb8","Gift wrapping and package presentation for the logistics network."),
 ("create_vibrant_vaults","Vibrant Vaults","▣","#c9a227","Item vaults in every colour and material, plus storage upgrades."),
 ("createornithopterglider","Ornithopter & Glider","✈","#5a9c88","Flight without an airship — gliders and flapping-wing craft."),
 ("createprism","Prism","◈","#8f7fa8","Light, optics and prismatic machinery."),
 ("create_optical","Optical","◉","#8f7fa8","Optical sensors, lenses and light-based automation."),
 ("create_pattern_schematics","Pattern Schematics","▦","#9a978c","Schematic tooling and pattern-based building aids."),
 ("create_tweaked_controllers","Tweaked Controllers","⎈","#b5673a","Better linked controllers for driving contraptions."),
 ("create_aquatic_ambitions","Aquatic Ambitions","≋","#5a9c88","Underwater machinery and a channeling process for aquatic resources."),
 ("create_deep_dark","Deep Dark","⌁","#5a7a8f","Sculk-themed machinery and deep dark resources."),
 ("create_dragons_plus","Dragons Plus","⟠","#8f7fa8","Dragon-themed processing, including an ending recipe type."),
 ("create_fantasizing","Fantasizing","✦","#8f7fa8","Fantasy-flavoured additions to Create's tech tree."),
 ("create_mob_spawners","Mob Spawners","☗","#7f6a4a","Automated, Create-powered mob spawning."),
 ("create_blaze_burner_fuels","Blaze Burner Fuels","⌇","#b5673a","More fuels and heat tiers for blaze burners."),
 ("create_generators","Generators","⌘","#c9a227","Additional stress-generating machines."),
 ("rubberworks","Rubberworks","◍","#5a7a5a","Rubber trees, sapping and elastic materials."),
 ("i_architecture","Immersive Architecture","☗","#8f7f5f","Architectural blocks and structural detailing."),
 ("pipeorgans","Pipe Organs","♪","#c9a227","Working pipe organs powered by Create air and rotation."),
 ("stockmarket","Stock Market","◎","#c9a227","Trade shares and speculate on commodity prices."),
 ("tradeworks","Tradeworks","◎","#c9a227","Trading infrastructure and merchant automation."),
 ("trading_floor","Trading Floor","◎","#c9a227","An automated trading hall for villager commerce."),
 ("sliceanddice","Slice & Dice","✂","#9a978c","A performance mod, not content — it makes Create's recipe lookups dramatically faster."),
 ("supplementaries","Supplementaries","☗","#7f6a4a","Decoration and utility blocks that Create packs almost always ship."),
]

# station display + hint for recipe types
STATIONS = {
 "minecraft:crafting_shaped":("Crafting Table","shaped"),
 "minecraft:crafting_shapeless":("Crafting Table","shapeless"),
 "minecraft:smelting":("Furnace",""),
 "minecraft:blasting":("Blast Furnace",""),
 "minecraft:smoking":("Smoker",""),
 "minecraft:campfire_cooking":("Campfire",""),
 "minecraft:stonecutting":("Stonecutter",""),
 "minecraft:smithing_transform":("Smithing Table",""),
 "create:mixing":("Mixing","Basin + Mechanical Mixer"),
 "create:compacting":("Compacting","Basin + Mechanical Press"),
 "create:pressing":("Pressing","Mechanical Press"),
 "create:crushing":("Crushing","Crushing Wheels"),
 "create:milling":("Milling","Millstone"),
 "create:cutting":("Cutting","Mechanical Saw"),
 "create:deploying":("Deploying","Deployer"),
 "create:item_application":("Item Application","Right-click the block by hand"),
 "create:filling":("Filling","Spout"),
 "create:emptying":("Emptying","Item Drain"),
 "create:splashing":("Washing","Encased Fan + Water"),
 "create:haunting":("Haunting","Encased Fan + Soul Fire"),
 "create:sandpaper_polishing":("Polishing","Sandpaper in a Deployer"),
 "create:sequenced_assembly":("Sequenced Assembly","Belt or Depot + Deployers"),
 "create:mechanical_crafting":("Mechanical Crafting","Mechanical Crafter grid"),
 "create:sawing":("Sawing","Mechanical Saw"),
 "farmersdelight:cutting":("Cutting Board",""),
 "farmersdelight:cooking":("Cooking Pot",""),
 "createaddition:rolling":("Rolling Mill",""),
 "createaddition:charging":("Charging",""),
 "createaddition:liquid_burning":("Liquid Burning",""),
 "mechanical_botany:insolating":("Insolator",""),
 "mechanical_botany:composting":("Composter",""),
 "dndesires:seething":("Seething",""),
 "dndesires:sanding":("Sanding",""),
 "dndesires:hydraulic_compacting":("Hydraulic Compacting",""),
 "create_aquatic_ambitions:channeling":("Channeling",""),
 "createdieselgenerators:wire_cutting":("Wire Cutting",""),
 "createdieselgenerators:hammering":("Hammering",""),
 "createdieselgenerators:compression_molding":("Compression Molding",""),
 "create_enchantment_industry:grinding":("Grinding",""),
 "create_new_age:energising":("Energising",""),
 "create_winery:maturing":("Maturing",""),
 "create_wrapped:wrapping":("Wrapping",""),
 "create_mob_spawners:spawning":("Spawning",""),
 "rubberworks:sapping":("Sapping",""),
 "create_dragons_plus:ending":("Ending",""),
}

# curated wiki text for the parts that matter, keyed by real item id
CURATED = {
"create:andesite_alloy":{
 "d":"The starter metal of Create and the thing you will craft more of than anything else. Every early machine, shaft, cogwheel and casing runs through it.",
 "o":["Craft Andesite with an Iron Nugget — this works in a plain crafting table from your first minute underground.","Automate it in a Basin under a Mechanical Mixer with the same two ingredients. Usually the first thing worth automating."],
 "t":["A Zinc Nugget works in place of the iron nugget, and zinc is often the one you have spare."]},
"create:wrench":{
 "d":"The tool you will never put down. Right-click to rotate a block; sneak-right-click to pick a machine up whole, keeping its filters, contents and configuration.",
 "t":["Sneak-right-click a configured machine to pocket it intact. Far faster than breaking it and re-setting every filter.","It also flips pump direction and reverses cogwheel rotation — the fix for half of all 'why isn't this working' moments."]},
"create:goggles":{
 "d":"Wear them in your helmet slot and look at any kinetic block: exact RPM, its stress cost, and your network's total load. Playing Create without these is playing blindfolded.",
 "t":["Look at a boiler with these on and it tells you exactly how many Steam Engines it will support. That one readout saves hours."]},
"create:andesite_casing":{
 "d":"A wooden block wrapped in andesite bracing. Casings are both a crafting ingredient and a tidy way to run a shaft through a wall.",
 "t":["This is made by holding Andesite Alloy and right-clicking a stripped log already placed in the world — not in a crafting grid. It trips up almost everyone.","Automate it with a Deployer holding Andesite Alloy, pointed at stripped logs on a belt."]},
"create:brass_ingot":{
 "d":"Copper and zinc melted together. Brass gates the smart half of Create — anything that filters, sorts, counts or decides is made of it.",
 "t":["Unlike Andesite Alloy this needs heat, which means a Blaze Burner, which means a trip to the Nether. That ordering is deliberate."]},
"create:cogwheel":{
 "d":"The small gear. Two cogwheels side by side pass rotation along and reverse its direction. A cogwheel meeting a Large Cogwheel changes the speed — this is how you gear up and down.",
 "t":["Small to large halves the speed. Large to small doubles it.","Cogwheels only mesh on their flat faces. Two large cogwheels can also mesh diagonally."]},
"create:water_wheel":{
 "d":"The first real power source: put it beside flowing water and it turns forever, free, with no fuel and no upkeep. Slow, but genuinely free.",
 "t":["It wants water flowing across its blades, not a still pool. Dig a two-block channel and drop a source at the high end.","Water arriving from opposite sides cancels out and the wheel sits dead. One direction only.","Gang two or three onto the same shaft — their capacity stacks. That's the standard early power bank."]},
"create:hand_crank":{
 "d":"You are the engine. Hold right-click to spin it; it produces a solid burst of rotation while you hold, and nothing when you let go.",
 "t":["Sneak while cranking to spin it the other way. That matters for pistons and pulleys."]},
"create:mechanical_press":{
 "d":"Slams down on whatever passes beneath it. Turns ingots into sheets, and finishes most sequenced assembly lines.",
 "t":["It needs a block of clearance beneath it and something to press on: a Depot, a Belt, or a Basin.","A press over a basin does compacting recipes instead of pressing."]},
"create:mechanical_mixer":{
 "d":"Sits above a Basin and stirs what's inside. Every alloy, most fluids and a great deal of food goes through here.",
 "t":["Mixers are stress-hungry. If your whole base stops the moment the mixer starts, that's why.","Put a Blaze Burner under the basin for heated recipes like brass."]},
"create:basin":{
 "d":"A bowl that holds items and fluids for Mixer and Press recipes. On its own it does nothing.",
 "t":["Output leaves the side the basin faces — sneak-right-click it with a Wrench to point it at your belt."]},
"create:crushing_wheel":{
 "d":"A pair of counter-rotating wheels that crush anything dropped between them, including you. Roughly doubles most ore yields.",
 "t":["They must be adjacent and must spin toward each other. If nothing happens, one is backwards — flip it with a Wrench or a Gearshift.","Drop items in from above and catch the output on a belt underneath."]},
"create:millstone":{
 "d":"A cheap, slow grinder you can run off a Hand Crank on day one. Weaker than Crushing Wheels, but available immediately.",
 "t":["Feed from the top, pull from the side or bottom with a funnel.","It takes rotation from the top or sides — a cogwheel underneath will not drive it."]},
"create:encased_fan":{
 "d":"Blows air. What the air passes through decides what it does: fire smelts, water washes, lava smelts faster, ice freezes. Also the cheapest item elevator in the game.",
 "t":["Put the fire, lava, water or ice directly in front of the fan; items in the airflow behind it get processed.","Bulk-washing crushed ore into nuggets is one of the biggest early yield jumps available."]},
"create:deployer":{
 "d":"A mechanical hand. It uses whatever item you give it on whatever is in front of it — right-click or left-click, your choice. This is the block that automates the un-automatable.",
 "t":["Sneak-right-click it with a Wrench to switch between use and punch mode.","Give it a filter so it only pulls the item you want off the belt behind it."]},
"create:mechanical_saw":{
 "d":"Facing up it fells any tree grown on top of it. Facing sideways it processes logs into planks at a better ratio than crafting.",
 "t":["Pointing up makes it a tree farm; pointing sideways makes it a processing machine on a belt.","Mounted on a moving contraption it chops everything it drives through."]},
"create:mechanical_drill":{
 "d":"Breaks the block in front of it, slowly. On its own it's a novelty. Bolted to a moving contraption it becomes a quarry.",
 "t":["Faster rotation means faster breaking — but stress cost scales with speed, so a geared-up drill is expensive.","A row of drills on a gantry or piston is the classic Create quarry."]},
"create:precision_mechanism":{
 "d":"The prestige component. It cannot be hand-crafted — it needs a Sequenced Assembly line, so you have to build a working factory to make the part that unlocks the good machines. The best-designed gate in Create.",
 "t":["The sequence runs five loops. Chance-based outputs mean you will get scrap — feed the failures back in.","Build it once by hand on a depot to understand it, then automate with a belt loop."]},
"create:steam_engine":{
 "d":"The end-game power source. Attach engines to a multiblock boiler built from Fluid Tanks, heat it, feed it water, and it produces stress capacity far beyond wind or water.",
 "t":["Heat, water supply and tank size all have to scale together. The goggles readout on the boiler tells you which one is holding you back.","Heat tiers: passive, a lit Blaze Burner, then a Blaze Burner fed Blaze Cakes for superheat."]},
"create:blaze_burner":{
 "d":"A blaze in a bucket. The heat source under every heated Basin recipe and every boiler.",
 "t":["A burner left unfed goes out and your brass line quietly stops. Automate fuel into it with a funnel."]},
"create:mechanical_arm":{
 "d":"A robot arm that picks from designated inputs and places into designated outputs, each with its own filter. Create's answer to complicated sorting.",
 "t":["Hold it and right-click the blocks you want as inputs, sneak-right-click for outputs, then place it.","Its reach is limited — keep the whole cluster tight."]},
"create:mechanical_crafter":{
 "d":"Automated crafting. Arrange several in a grid matching your recipe's shape, point their arrows so every path flows to one exit, and feed each slot its ingredient.",
 "t":["Use a Wrench to rotate each crafter's arrow. Every path must lead to the same single output.","Feed the grid with a Mechanical Arm or a wall of filtered Brass Funnels."]},
"create:rotation_speed_controller":{
 "d":"Set an exact RPM with a dial instead of chaining gears. Place it under a Large Cogwheel and type the number you want. The most convenient block in the mod.",
 "t":["Remember the stress bill scales with the speed you dial in."]},
"create:elevator_pulley":{
 "d":"A proper elevator. Set contacts at each floor, ride the platform, and call it with buttons.",
 "t":["Place Elevator Contacts in a vertical column beside the shaft, one per floor. Name them and the names show on the call panel.","The platform must be glued into one contraption like anything else."]},
"create:andesite_funnel":{
 "d":"The basic input and output block. It moves items between an inventory and a belt or depot, in either direction, with no filter — it takes whatever comes.",
 "t":["The direction matters. Use a Wrench to flip whether it's inserting or extracting.","Upgrade to a Brass Funnel the moment you need it to be picky about what passes through."]},
"create:andesite_tunnel":{
 "d":"A belt cover that splits exactly one item off any passing stack whenever it has a side connection, letting the rest continue down the belt. The simplest way to pull one ingredient off a shared line without disturbing the rest.",
 "t":["No filter, no configuration — it always takes one item per stack that passes through. For anything picky, use a Brass Tunnel instead.","Tunnels connect belt to belt. Funnels connect belt to inventory. That's the whole distinction."]},
"create:brass_tunnel":{
 "d":"The filtered, configurable version of a belt tunnel. Set a distribution mode and it decides how items get divided across multiple exits: split evenly, round robin, prefer the nearest exit, or several others.",
 "t":["Filters sit on each open side — inbound filters block anything that doesn't match, outbound filters sort by type.","Brass Tunnels on parallel belts can link into a group and pull from a shared source at a synchronized rate, which keeps several lines fed evenly instead of draining unevenly."]},
"create:brass_funnel":{
 "d":"An Andesite Funnel with a filter slot and an amount setting. This is where item sorting actually begins.",
 "t":["Right-click the filter to invert it into a blacklist.","A row of differently-filtered brass funnels over one belt is the classic Create sorter."]},
"create:belt_connector":{
 "d":"Create's conveyor. Place two shafts and connect them with this to string a belt between them. Items ride it; so do you.",
 "t":["Belts run flat, diagonally at 45 degrees, or vertically. Only one shaft needs power.","A belt passing under a press or through crushing wheels processes what rides on it."]},
"create:mechanical_bearing":{
 "d":"Spins an attached structure. Point it at your build, right-click to assemble, and the whole thing rotates.",
 "t":["If it refuses to assemble, something isn't glued or is still touching a block it shouldn't."]},
"create:portable_storage_interface":{
 "d":"Lets a stationary inventory trade items with whatever's riding a passing contraption, without the contraption needing to stop. Mount one on the moving inventory and place a matching one nearby in its path; when they line up they connect just long enough to exchange items, then the contraption carries on.",
 "t":["Leave a gap of 1–2 blocks between the two interfaces — that's the connection range.","Powering the stationary one with redstone blocks the connection, a clean way to pause collection on demand.","Only needs an Andesite Casing and a Chute — no brass required, despite feeling like a late-game part."]},
"create:rope_pulley":{
 "d":"Lowers and raises a structure on a rope. The simplest vertical contraption and the basis of most early lifts and mine shafts.",
 "t":["Pair it with a Gearshift on a redstone pulse to send it back up."]},
"create:mechanical_piston":{
 "d":"A piston that pushes an entire structure rather than one block. Add Piston Extension Poles behind it to set the travel distance.",
 "t":["Everything you want moved must be joined with Super Glue or Chassis blocks."]},
"create:stressometer":{
 "d":"Reads how much of your network's stress capacity is in use. Put one on every power bank you build — it turns overstress from a mystery into a number.",
 "t":["Wear Goggles and look at it for the exact figure rather than the needle."]},
"create:speedometer":{
 "d":"Reads the RPM of the shaft it's attached to. Wear Goggles and look at it for an exact number.",
 "t":[]},
"create:shaft":{
 "d":"A plain rotating rod. Shafts carry rotation in a straight line, unchanged in speed and direction, and cost almost nothing.",
 "t":[]},
"create:large_cogwheel":{
 "d":"The big gear. Pair it with a small Cogwheel to halve or double rotation speed depending on which drives which.",
 "t":[]},
"create:copper_casing":{"d":"The fluid-tier casing. Anything that moves liquid tends to be built on this.","t":["Made by right-clicking a stripped log with a Copper Sheet."]},
"create:brass_casing":{"d":"The smart-tier casing. If a machine makes a decision, it's wearing brass.","t":["Made by right-clicking a stripped log with a Brass Sheet."]},
"create:fluid_tank":{"d":"Stores liquid, and stacks with its neighbours into one large multiblock. That same multiblock is the boiler for Steam Engines.","t":["Wear Goggles and look at a boiler to read its heat level, water supply and engine capacity."]},
"create:mechanical_pump":{"d":"Pushes fluid along a pipe network. Pipes do nothing without one somewhere in the line.","t":["Sneak-right-click with a Wrench to reverse flow direction."]},
"create:windmill_bearing":{"d":"Point it at the sky, build a sail assembly on it, and right-click to start it turning. Output scales with sail count.","t":["There's a minimum sail count before it will start — build generously.","Weather and biome are irrelevant; only the number of sails matters."]},
"create:sequenced_gearshift":{"d":"A programmable rotation controller. Give it a list of instructions — turn 90 degrees, wait, reverse — and it drives a contraption through the routine on one redstone pulse.","t":[]},
"create:redstone_link":{"d":"Wireless redstone. Put two items in a link's frequency slots; any other link with the same pair is connected to it.","t":[]},
"create:display_link":{"d":"Reads a value from a block — item counts, tank levels, stress, time — and writes it to a sign or Display Board.","t":[]},
"create:gantry_carriage":{"d":"Rides along a Gantry Shaft carrying a structure. Unlike a piston it moves continuously and can travel any distance.","t":["Two gantries at right angles give you a proper two-axis quarry head."]},
"create:clutch":{"d":"A redstone-controlled switch in a rotation line. Powered, it cuts the rotation dead.","t":[]},
"create:gearshift":{"d":"Powered, it reverses the direction of rotation. This is how pistons and pulleys travel back.","t":[]},
"create:item_vault":{"d":"A big storage box that merges with its neighbours into one shared inventory. Cheap, ugly, and exactly what a factory buffer should be.","t":[]},
"create:depot":{"d":"A single item-sized table — the stationary alternative to a belt for machines that process one thing at a time.","t":[]},
"create:chute":{"d":"A vertical item pipe. It pulls items down; put an Encased Fan beneath it and it pushes them up instead.","t":[]},
"create:packager":{"d":"Wraps items from an attached inventory into packages that ship through the logistics network. The entry point to Create's factory automation.","t":[]},
"create:stock_ticker":{"d":"The terminal. Right-click to browse everything registered on your network and order items delivered to you.","t":[]},
"create:stock_link":{"d":"Attaches to a Packager and registers its inventory with a Stock Ticker so the network knows what you have.","t":[]},
"create:redstone_requester":{"d":"Automatically orders a set list of items from the network on a redstone pulse. Automation that restocks itself.","t":[]},
"create:factory_gauge":{"d":"Links a machine's output to the ingredients it needs, so the chain only runs when something downstream asks for the product.","t":[]},
"create:chain_conveyor":{"d":"Overhead chains that carry packages long distances between anchor points. Cheap, fast, and it looks superb strung across a base.","t":["You can ride them — grab on and travel with your packages."]},
"create:rose_quartz":{"d":"A pink crystal made rather than mined. It forces you to build a Deployer chain, which is deliberate.","t":["Polish it further with sandpaper in a Deployer to get Polished Rose Quartz."]},
"create:electron_tube":{"d":"A little vacuum tube — Create's stand-in for a logic chip. It appears in anything that senses or transmits.","t":[]},
"create:zinc_ingot":{"d":"A pale ingot that does little alone. Mixed with copper it becomes brass, which is where the mid-game begins.","t":["Zinc ore is common in ordinary stone below about Y 70. Don't hoard it."]},
"create:iron_sheet":{"d":"A pressed iron plate. Sheets are Create's way of making you build a machine before you can build better machines.","t":[]},
"create:brass_sheet":{"d":"A pressed brass plate, and the gate to brass casings and every brass-tier machine.","t":[]},
"create:copper_sheet":{"d":"A pressed copper plate — the key to copper casings and the whole fluid system.","t":[]},
"create:golden_sheet":{"d":"A pressed gold plate. You need few, but the ones you need matter.","t":[]},
"create:railway_casing":{"d":"The train-tier casing, and noticeably expensive. Every piece of rolling stock runs through it.","t":[]},
"create:steam_whistle":{"d":"Mounted on a boiler, it sounds. Purely for character, and worth every ingot.","t":[]},
}

GUIDES = {
"basics":{"title":"Create 101","eyebrow":"Field Manual · Section One",
 "lede":"Create runs on one idea: rotation. Understand that and the other two hundred mods make sense.",
 "body":[
  {"h":"Rotation is the resource"},
  {"p":"There is no power grid and no cables. A source spins a shaft, the shaft spins machines, the machines do work. Two numbers describe every network."},
  {"p":"<b>Speed</b> is measured in RPM. It sets how fast a machine works, and some machines refuse to run below a threshold. <b>Stress</b> is measured in stress units. Every source adds capacity; every machine consumes it. Go over capacity and the whole network stops dead until you remove load or add a source."},
  {"note":"Put a [[create:stressometer|Stressometer]] on every power bank and wear [[create:goggles|Engineer's Goggles]]. You'll never wonder why a machine stopped again."},
  {"h":"The four things to make first"},
  {"p":"In order, and none of them need power:"},
  {"list":["[[create:andesite_alloy|Andesite Alloy]] — andesite plus an iron nugget. Make a stack. Make two.",
           "[[create:wrench|The Wrench]] — rotates blocks and pockets machines with their settings intact.",
           "[[create:goggles|Engineer's Goggles]] — puts speed and stress numbers on everything you look at.",
           "[[create:andesite_casing|Andesite Casing]] — hold Andesite Alloy and right-click a stripped log on the ground. Not a crafting recipe, which catches almost everyone out."]},
  {"h":"Casings, in three tiers"},
  {"p":"Casings signal progression. Each is a stripped log with a metal applied by hand or by [[create:deployer|Deployer]]."},
  {"list":["[[create:andesite_casing|Andesite Casing]] — presses, mixers, drills, saws, fans. The whole tier-one set.",
           "[[create:copper_casing|Copper Casing]] — anything that moves fluid, plus [[create:steam_engine|Steam Engines]].",
           "[[create:brass_casing|Brass Casing]] — anything that filters, sorts or decides."]},
  {"h":"Getting to brass"},
  {"p":"[[create:brass_ingot|Brass]] is copper and zinc mixed <i>with heat</i>. Heat means a [[create:blaze_burner|Blaze Burner]], which means a Nether trip for blaze rods. Once you have brass you unlock filters, [[create:deployer|Deployers]] and [[create:mechanical_arm|Arms]], and the game changes character."},
  {"h":"Speed and gearing"},
  {"p":"A [[create:cogwheel|Cogwheel]] meeting a [[create:large_cogwheel|Large Cogwheel]] halves the speed; large driving small doubles it. Chain them for anything up to the 256 RPM cap. Once you can afford a [[create:rotation_speed_controller|Rotation Speed Controller]] you can skip all of it and type a number."},
  {"warn":"Faster is not free. Stress cost scales with speed, so doubling a drill's RPM doubles what it takes out of your budget."},

  {"h":"Moving items"},
  {"p":"A rotation network is only half of Create. The other half is getting items from A to B, and the mod gives you four tools for it depending on how much control you need."},
  {"list":[
   "[[create:belt_connector|Belts]] — the default. Right-click two shafts with a belt to string one between them; only one end needs power, and everything on it moves at the same speed.",
   "[[create:andesite_funnel|Andesite Funnels]] — move items between an inventory and a belt or depot, no filter. The basic connector between a machine and everything else.",
   "[[create:brass_funnel|Brass Funnels]] — an Andesite Funnel with a filter slot. This is where sorting starts: whitelist or blacklist an item, and stack several with different filters over one belt to sort it.",
   "[[create:andesite_tunnel|Andesite Tunnels]] — cover a belt and split exactly one item off any passing stack toward a side connection, leaving the rest to continue. Good for pulling one ingredient off a shared line.",
   "[[create:brass_tunnel|Brass Tunnels]] — the filtered, configurable version. Several distribution modes decide how items divide across multiple exits, and tunnels on parallel belts can link into a group that all draw from one source at a synchronized rate.",
   "[[create:chute|Chutes]] — vertical belts. Items fall through one on their own; add an Encased Fan at either end and they travel up instead."]},
  {"note":"Funnels connect a belt to an inventory. Tunnels connect a belt to another belt. That's the whole distinction, and it's the thing most people mix up first."}]},

"starter":{"title":"First Steps to Automation","eyebrow":"Field Manual · Section Two",
 "lede":"Two builds that take you from hand-cranking to genuinely automated. Do them in this order.",
 "body":[
  {"h":"Build one — the hand-cranked press"},
  {"p":"Your first machine needs no power source at all, and it makes the [[create:iron_sheet|sheets]] every later machine wants."},
  {"steps":[
   {"b":"Place a [[create:depot|Depot]]","t":"A single item-sized table. Items sit on it one at a time."},
   {"b":"Put a [[create:mechanical_press|Mechanical Press]] two blocks above it","t":"Leave one air block between press and depot. That gap is where the pressing happens."},
   {"b":"Run a [[create:shaft|Shaft]] out of the press's side","t":"Attach a [[create:hand_crank|Hand Crank]] to the far end."},
   {"b":"Drop an iron ingot on the depot and hold right-click on the crank","t":"The press comes down and you get an Iron Sheet. That's a factory."},
   {"b":"When cranking gets old","t":"Swap the crank for a [[create:water_wheel|Water Wheel]] and put a funnel on the depot to feed it from a chest."}]},
  {"schem":["  [Press]        <- powered by shaft","     |","   ( gap )       <- items get pressed here","     |","  [Depot] <--- funnel from chest","","  Press --shaft--> [Hand Crank]   (later: Water Wheel)"]},
  {"h":"Build two — free permanent power"},
  {"p":"Hand-cranking gets old fast. A [[create:water_wheel|Water Wheel]] gives you rotation that never stops and costs nothing to run — the power source every farm and machine in this manual assumes you have."},
  {"steps":[
   {"b":"Dig a channel two blocks long and drop one water source at the high end","t":"You want visibly flowing water. A still pool turns nothing."},
   {"b":"Place the [[create:water_wheel|Water Wheel]] so the flow crosses its blades","t":"Flow arriving from both sides cancels out and the wheel sits dead. One clean direction of flow only."},
   {"b":"Gang two or three wheels on the same [[create:shaft|Shaft]]","t":"Capacity stacks. One wheel alone is a small stress budget; a bank of them carries real machines."},
   {"b":"Run the [[create:shaft|Shaft]] up to where you need it","t":"This shaft is now your base's power. Point it at the press from Build one, or carry it to whatever you build next."}]},
  {"note":"Put a [[create:stressometer|Stressometer]] on the line and wear [[create:goggles|Engineer's Goggles]]. When the needle nears the top, add a wheel before you add a machine — that's the whole discipline of running a network."},
  {"h":"Where to go next"},
  {"p":"You now have sheets and free power. The next move is to put that shaft to work: head to <b>Farms &amp; Contraptions</b> and build a [[create:andesite_alloy|Andesite Alloy]] line or a crop farm, both of which run off exactly the water wheel you just placed. When you're ready to leave tier one, go get blaze rods and start on [[create:brass_ingot|Brass]] in <b>Starter Machines</b>."}]},

"machines":{"title":"Starter Machines","eyebrow":"Field Manual · Section Three",
 "lede":"The two things that unlock the rest of the pack: a heat source for brass, and the Mechanical Crafting grid for recipes a crafting table can't make.",
 "body":[
  {"note":"Looking to automate a resource — trees, crops, ore, andesite? Those builds now live in <b>Farms &amp; Contraptions</b>. This section is the machinery underneath them."},
  {"h":"A basic brass line"},
  {"p":"[[create:brass_ingot|Brass]] is copper and zinc mixed <i>with heat</i>, which is the one ingredient a Basin and Mixer can't supply on their own — you need a [[create:blaze_burner|Blaze Burner]] underneath, and that means a trip to the Nether."},
  {"steps":[
   {"b":"Kill a blaze at a Nether fortress","t":"Bring a water bucket — dousing yourself stops the fire damage — and watch for other fortress mobs while you fight it."},
   {"b":"Craft an [[create:blaze_burner|Empty Blaze Burner]]","t":"Netherrack plus four [[create:iron_sheet|Iron Sheets]] at a crafting table."},
   {"b":"Right-click a live blaze with the Empty Blaze Burner","t":"This captures it. You don't need to keep fighting blazes afterward — one burner runs forever once it's fed."},
   {"b":"Place the burner and light it with any fuel","t":"Coal or charcoal is fine for now. A lit burner heats whatever basin sits directly above it."},
   {"b":"Stack a [[create:basin|Basin]] on top, then a [[create:mechanical_mixer|Mechanical Mixer]] above that","t":"Same arrangement as the andesite alloy line above, just with a heat source underneath."},
   {"b":"Feed in copper and zinc ingots, one of each","t":"One mix gives 2 Brass Ingots in this pack. Copper is common everywhere; zinc ore shows up in ordinary stone below about Y 70."}]},
  {"warn":"A burner left unfed goes out, and your brass line stops producing without any obvious error — it just quietly sits there. Automate fuel into it with a funnel once you trust the rest of the line."},
  {"h":"Mechanical Crafting"},
  {"p":"Some of the pack's key items — [[create:crushing_wheel|Crushing Wheels]] first among them — have no crafting-table recipe at all. The only way to build them is Mechanical Crafting, and once you've set it up once you can automate almost any shaped recipe the same way."},
  {"p":"A [[create:mechanical_crafter|Mechanical Crafter]] is a crafting-table square that runs on rotation instead of your hands. Arrange several in the same shape as the recipe, load each one with its own ingredient, point every arrow with a [[create:wrench|Wrench]] so they all feed toward one shared output, then power the grid."},
  {"steps":[
   {"b":"Build the grid in the recipe's shape","t":"For [[create:crushing_wheel|Crushing Wheels]]: a 5×5 of Mechanical Crafters with the corners empty — 21 total. The outer ring loaded with [[create:andesite_alloy|Andesite Alloy]], four with any planks, one dead centre with any stone. That makes 2 wheels per run."},
   {"b":"Point every crafter's arrow at the same shared output","t":"Wrench each one until its arrow lines up. If even a single crafter points the wrong way, the whole grid refuses to output anything — the usual reason a crafter grid \"does nothing.\""},
   {"b":"Power the grid and collect","t":"A funnel at the output face carries the finished item into a chest. Feed the input crafters from belts and the grid runs on its own."}]},
  {"note":"JEI shows you this same kind of grid for any Mechanical Crafting recipe — press R over an item to see it. The technique works everywhere, not just for Crushing Wheels."},
  {"p":"Built a pair of [[create:crushing_wheel|Crushing Wheels]]? Turn them into an ore-doubling line over in <b>Farms &amp; Contraptions → Iron &amp; Ore Doubling</b>."}]},

"advanced":{"title":"Advanced Works","eyebrow":"Field Manual · Section Four",
 "lede":"Where the pack opens up: real power, real logistics, and the machines worth the grind.",
 "body":[
  {"h":"Steam power"},
  {"p":"Water and wind carry you a long way, but a boiler is a different order of magnitude."},
  {"steps":[
   {"b":"Stack [[create:fluid_tank|Fluid Tanks]] into a block","t":"They merge into one multiblock. Bigger boiler, more engines it supports."},
   {"b":"Put [[create:blaze_burner|Blaze Burners]] underneath","t":"Passive heat is weak, a lit burner better, a burner fed Blaze Cakes is superheated."},
   {"b":"Pipe water in with a [[create:mechanical_pump|Mechanical Pump]]","t":"It needs continuous supply. A bottomless water source plus a pump is fine."},
   {"b":"Attach [[create:steam_engine|Steam Engines]] to the tank sides","t":"Each adds a shaft output. Look at the boiler with goggles to see how many it will carry."}]},
  {"note":"Heat, water and tank size all scale together. The goggles readout tells you which of the three is the bottleneck."},
  {"h":"Elevators"},
  {"steps":[
   {"b":"Build the platform and glue it together","t":"It behaves like any contraption — one connected structure."},
   {"b":"Place an [[create:elevator_pulley|Elevator Pulley]] above with rope run down","t":"Power the pulley with a shaft."},
   {"b":"Put Elevator Contacts in a vertical column beside the shaft","t":"One per floor. Name each and the names appear on the call panel."},
   {"b":"Ride it","t":"Call buttons on each floor, and it stops level every time."}]},
  {"h":"Quarries"},
  {"p":"A row of [[create:mechanical_drill|Mechanical Drills]] on a [[create:gantry_carriage|Gantry Carriage]] sweeping across a piston-driven frame gives a two-axis quarry. Gear the drills up with a [[create:rotation_speed_controller|Rotation Speed Controller]] — much faster breaking, much larger stress bill."},
  {"warn":"Quarries are the most common cause of whole-base overstress. Put them on their own power source, or at least their own [[create:clutch|Clutch]] so you can switch them off."},
  {"h":"The logistics network"},
  {"p":"Create 6 added a proper factory layer — [[create:packager|Packagers]], [[create:stock_ticker|Stock Tickers]] and overhead [[create:chain_conveyor|Chain Conveyors]] that replace hundreds of belts with on-demand delivery — and this pack leans on it hard. It's big enough to be its own section: see <b>The Logistics Network</b> for the full build."},
  {"h":"Power beyond steam"},
  {"p":"This pack ships several alternatives. Diesel Generators adds an oil-to-combustion chain with enormous output. Crafts & Additions lets you convert rotation to Forge Energy and back, so you can run a shaft-free remote machine off a cable. New Age goes nuclear. All of them plug into the same stress network."}]},

"logistics":{"title":"The Logistics Network","eyebrow":"Field Manual · Section Five",
 "lede":"Create 6's factory layer. Once a base outgrows belts, this is what replaces them — request-driven delivery instead of a permanent line for every item.",
 "body":[
  {"h":"Why belts stop scaling"},
  {"p":"A belt is a dedicated road for one flow of items. That's fine for a handful of machines, but a mature base wants hundreds of items on demand and can't afford a permanent belt to each one. The logistics network moves items only when something asks for them, over shared infrastructure, so one set of chains serves the whole base."},
  {"p":"Everything travels as a <b>package</b> — a wrapped bundle of items with a written address. Machines make packages, the network routes them, and something at the far end unwraps them. Four ideas cover the whole system."},
  {"h":"The four pieces"},
  {"list":[
   "[[create:packager|Packager]] — bolts onto any inventory and wraps its contents into an addressed package. This is how items <i>enter</i> the network.",
   "[[create:stock_link|Stock Link]] — registers an inventory (through its Packager) with the network, so the terminal knows that stock exists and can pull from it.",
   "[[create:stock_ticker|Stock Ticker]] — the shop counter. A searchable list of everything every linked inventory holds, with a keyboard: type what you want, how many, and it dispatches the order.",
   "[[create:chain_conveyor|Chain Conveyor]] — overhead chains strung between posts that carry packages across the base. Packages hop from chain to chain at junctions to reach their address. You can clip on and ride them yourself."]},
  {"note":"A [[create:packager|Packager]] can only wrap what it can reach. Put it on the face of a chest, a [[create:fluid_tank|vault]] or a barrel, and give that inventory the stock you want the network to be able to hand out."},
  {"h":"Getting packages moving"},
  {"steps":[
   {"b":"Stick a [[create:packager|Packager]] on each storage inventory","t":"Every chest or vault you want the network to draw from needs one. It wraps items out and unwraps deliveries in."},
   {"b":"Attach a [[create:stock_link|Stock Link]] to each Packager","t":"This is what tells the network the inventory exists. An unlinked Packager can still wrap on command but won't show up in the terminal's stock list."},
   {"b":"Place a [[create:stock_ticker|Stock Ticker]] where you'll stand","t":"Right-click it to open the terminal. It lists the combined contents of every linked inventory in range of the connected chain network."},
   {"b":"Run [[create:chain_conveyor|Chain Conveyors]] between them","t":"Connect a chain from the Ticker's network out to each Stock Link's location. Chains bridge gaps and turn corners at connection posts; a package finds its own way across."},
   {"b":"Order something","t":"Search the Ticker, set a count, confirm. The holding inventory packages it, the chains carry it to the Ticker's output, and it arrives wrapped."}]},
  {"h":"Delivery to a place, not just the counter"},
  {"p":"A [[create:package_frogport|Frogport]] or a coloured [[create:white_postbox|Postbox]] is a drop-off point with its own address. Address a package to that name and the network routes it there instead of back to the Ticker — deliveries to a remote build site, an airport, another dimension's portal. The Frogport's mechanical frog physically hops packages on and off the chain."},
  {"note":"Give every drop-off a distinct address and keep them short. The address is how the network decides where a package goes; two points sharing a name is the usual reason a delivery ends up at the wrong one."},
  {"h":"On-demand crafting"},
  {"p":"The real payoff is a network that <i>makes</i> things it doesn't have in stock. This is the [[create:redstone_requester|Redstone Requester]] and [[create:factory_gauge|Factory Gauge]] layer, and it turns the whole base into one assembler."},
  {"list":[
   "[[create:redstone_requester|Redstone Requester]] — asks the network for a fixed order on a redstone pulse. Wire it to a machine that's run low and it restocks that machine's inputs automatically.",
   "[[create:factory_gauge|Factory Gauge]] — links a product to the ingredients it's made from. Chain gauges across a multi-step recipe and ordering the final item pulls each stage's inputs in turn, so nothing runs until there's demand for it.",
   "[[create:repackager|Repackager]] — re-wraps arriving packages into the exact stacks a downstream recipe wants, so a crafter gets clean inputs instead of whatever bundle showed up."]},
  {"p":"Set up right, you type one item into the [[create:stock_ticker|Ticker]] and the network crafts it from raw materials three steps back, pulling each ingredient only as the stage above it calls for it. That's the endgame this whole system builds toward."},
  {"warn":"The logistics parts want [[create:precision_mechanism|Precision Mechanisms]], which are a brass-and-gold grind. Don't tear out working belts to reach it — build the network alongside them and migrate flows over one at a time as it comes online."}]},
}

# ---------------- Farms ----------------
# The Works: a growing catalogue of contraptions that make things.
# Each entry is a farm type shown as a token on the Farms index, linking to
# its own build page. "glyph"/"col" style the token to match the mod index.
# Body blocks use the same vocabulary as GUIDES (h/p/note/warn/list/schem/steps).
# Keep the keys such that display order is alphabetical by title.
FARMS = {
"andesite_alloy":{"title":"Andesite Alloy","glyph":"▩","col":"#9a978c",
 "sub":"Basin + mixer · no heat","yields":"Andesite Alloy, endlessly",
 "lede":"The first thing worth fully automating. Andesite Alloy gates casings, shafts and half the tier-one recipes, so a line that makes it while you do something else removes the bottleneck on everything.",
 "body":[
  {"p":"[[create:andesite_alloy|Andesite Alloy]] is andesite plus an iron nugget, mixed. No heat, so this is the simplest automatic production line in the pack and a good first one to build."},
  {"steps":[
   {"b":"Place a [[create:basin|Basin]] with a [[create:mechanical_mixer|Mechanical Mixer]] directly above it","t":"Leave the standard gap the Mixer wants. Power the Mixer from a shaft — a single [[create:water_wheel|Water Wheel]] is plenty."},
   {"b":"Feed andesite and iron nuggets in from above","t":"Two filtered [[create:brass_funnel|Brass Funnels]] over the basin, one whitelisting andesite and one whitelisting iron nuggets, or a single belt carrying both."},
   {"b":"Point the basin's output at a belt","t":"Sneak-right-click the basin with a [[create:wrench|Wrench]] to choose the output side, then run a belt into a chest."},
   {"b":"Keep the inputs fed","t":"A crusher turning cobble into andesite, or a raw andesite stockpile, plus iron nuggets from ore doubling. The mixer only runs when both ingredients are present, so it idles safely when it runs dry."}]},
  {"note":"No heat source is needed here — that's what makes Andesite Alloy easier to automate than brass. If your mixer refuses to run, it's a power or a missing-ingredient problem, never a heat one."},
  {"h":"Fully renewable, from cobblestone"},
  {"p":"Both inputs can be manufactured, so a mature line needs no mining at all. Iron nuggets come from the <b>Iron (from Gravel)</b> farm — the wash by-product is exactly what this basin wants. And andesite stone itself can be made: compact flint + gravel with a bit of lava in a [[create:mechanical_press|Press]] over a [[create:basin|Basin]]. Wire a [[minecraft:cobblestone|cobble]] generator into both and the whole line runs on stone, at roughly 9–10 cobble per finished alloy."},
  {"warn":"A Mixer's stress cost scales with speed. There's no reason to gear this line up; run it slow and it sips from your budget while still out-producing what you can use by hand."}]},

"cobblestone":{"title":"Cobblestone & Gravel","glyph":"▦","col":"#7f7a70",
 "sub":"Lava + water · drill","yields":"Cobble, gravel, sand, flint",
 "lede":"Endless stone with no digging, and a crushing stage that turns it into the gravel, sand and flint a dozen recipes quietly need.",
 "body":[
  {"h":"The generator"},
  {"p":"A lava source meeting flowing water makes cobblestone where they touch. A [[create:mechanical_drill|Mechanical Drill]] aimed at that spot breaks the cobble the instant it forms, and the block regenerates forever."},
  {"steps":[
   {"b":"Build the classic generator block","t":"A one-block gap between a lava source and a water source, arranged so cobble forms in the gap. Any vanilla cobble-gen layout works."},
   {"b":"Aim a [[create:mechanical_drill|Mechanical Drill]] at the cobble spot","t":"Power it from a shaft. The drill breaks the block on contact and the lava/water make a fresh one immediately."},
   {"b":"Catch the drops","t":"A belt or a [[create:andesite_funnel|Funnel]] under the break point feeds a chest. One drill is a steady trickle; a row of generators and drills is a flood."}]},
  {"h":"Crushing it further"},
  {"p":"Raw cobble is rarely the goal — the value is downstream."},
  {"list":[
   "[[create:crushing_wheel|Crushing Wheels]] or a [[create:millstone|Millstone]] turn cobble into gravel, and gravel into sand.",
   "Crushing gravel also yields the occasional flint, which the Millstone route gives more patiently for the price of one cheap machine.",
   "Sand feeds glass; gravel feeds concrete and paths. A cobble generator behind a crusher quietly supplies all three."]},
  {"note":"A single [[create:millstone|Millstone]] is the cheapest entry point — it needs no casing pair and runs off one shaft. Step up to [[create:crushing_wheel|Crushing Wheels]] only when the throughput matters."},
  {"warn":"Drills breaking blocks every tick add up. Put the generator on its own [[create:clutch|Clutch]] so you can switch it off, or a stockpile latch so it stops once the output chest is full."}]},

"crops":{"title":"Crops (Wheat & Vegetables)","glyph":"❦","col":"#5a9c88",
 "sub":"Bearing + harvester","yields":"Wheat, carrots, potatoes, beetroot",
 "lede":"The classic first farm: a [[create:water_wheel|Water Wheel]] spinning a [[create:mechanical_bearing|Bearing]] that sweeps a harvester in a slow circle over a field. Free power, replanted automatically.",
 "body":[
  {"h":"The rotating harvester"},
  {"steps":[
   {"b":"Dig a channel and drop one water source at the high end","t":"You want visibly flowing water across the wheel's blades. A still pool turns nothing, and flow arriving from both sides cancels out."},
   {"b":"Gang two or three [[create:water_wheel|Water Wheels]] on one [[create:shaft|Shaft]]","t":"Capacity stacks. One wheel alone won't carry a harvester swinging through a full field for long."},
   {"b":"Run the shaft to a [[create:mechanical_bearing|Mechanical Bearing]] pointing sideways","t":"Build an arm out from the bearing and hang a [[create:mechanical_harvester|Mechanical Harvester]] on the end, facing the crops at head height."},
   {"b":"Super Glue the whole arm into one piece","t":"Everything the bearing carries must be a single glued structure or it won't assemble."},
   {"b":"Right-click the bearing to assemble, then power it","t":"The arm sweeps the field, cutting mature crops and leaving the seeds to replant themselves."},
   {"b":"Catch the drops","t":"Run a belt along the field edge into a chest, or lay the field over a hopper floor."}]},
  {"schem":["   [Bearing]===arm===[Harvester]","      |                    \\","   [shaft]                  ( sweeps the field )","      |","  [Water Wheels]  <- flowing water"]},
  {"note":"Wheat, carrots, potatoes and beetroot all grow on farmland and all work with this one build — plant a mixed field and the same harvester cuts whichever blocks are mature."},
  {"warn":"If the bearing won't assemble, something on the arm is touching a block it shouldn't, or a piece isn't glued. One water wheel is a small budget too — put a [[create:stressometer|Stressometer]] on the line and add a wheel before the needle tops out."},
  {"h":"Scaling up — the linear farm"},
  {"p":"The carousel is capped by its radius. To feed a base, switch to a straight row of harvesters dragged across a rectangular field on a [[create:cart_assembler|Cart Assembler]] and minecart, tripped on a [[create:pulse_timer|Pulse Timer]]. It tiles to any length and width and is the standard high-output crop farm."},
  {"steps":[
   {"b":"Lay out 9×9 field blocks end to end, water in the centre of each","t":"One water source irrigates four blocks each way. Cover the water with a slab and torch so plants don't sit on it."},
   {"b":"Build a harvester bar on [[create:linear_chassis|Linear Chassis]]","t":"A ground row of chassis with a [[create:mechanical_harvester|Mechanical Harvester]] on each, a chest above to catch drops. Ctrl-[[create:wrench|Wrench]] the chassis to set sticky range to 1 so it only grabs its own bar."},
   {"b":"Mount the bar on a [[create:cart_assembler|Cart Assembler]] over a rail line","t":"Set the assembler to Lock Rotation. Powered rail out and back, a solid block at each end so the cart reverses and returns to start."},
   {"b":"Hand off drops with paired [[create:portable_storage_interface|Storage Interfaces]]","t":"One on the moving bar, one on the wall by the rail; a [[create:chute|Chute]] below the fixed one drops into storage as the cart passes."},
   {"b":"Time it with a [[create:pulse_timer|Pulse Timer]]","t":"A lever OFF starts the clock; set the interval to taste. Each pulse sends the bar across the field once."}]},
  {"note":"A four-plot linear farm like this runs to the order of ~570 crops and ~330 seeds an hour across wheat, carrots, potatoes and beetroot. If storage fills, the bar keeps harvesting but drops produce on the ground — size the output chest, or feed it into a vault or the logistics network."},
  {"h":"The planting alternative"},
  {"p":"For crops that don't replant from their own drops, add two [[create:deployer|Deployers]] to the bar or arm: one holding a hoe or bone meal, one holding seeds. This needs brass, so it's a second-generation upgrade — the harvester builds above get you farming long before then."}]},

"gold":{"title":"Gold from Cobblestone","glyph":"◈","col":"#e0b53a",
 "sub":"The long transmutation","yields":"Gold nuggets, from stone",
 "lede":"Create's showpiece farm: turn plain cobblestone into gold through a chain of crushing, washing, pressing and blasting. It's slow and gloriously over-engineered — the build that shows what the mod is really about.",
 "body":[
  {"p":"Every stage transforms the last, so the whole thing is one long belt. It runs on a [[minecraft:cobblestone|cobble]] generator at the head and drips gold out the far end — expect roughly 1.5 gold ingots per 512 cobblestone, so scale the front hard and be patient."},
  {"h":"The chain, stage by stage"},
  {"steps":[
   {"b":"Cobblestone → gravel","t":"A [[create:millstone|Millstone]] or [[create:crushing_wheel|Crushing Wheels]] on the cobble generator's output."},
   {"b":"Gravel → sand","t":"[[create:crushing_wheel|Crushing Wheels]] only here — a Millstone won't take gravel to sand. Flint and the odd clay ball come off as by-products."},
   {"b":"Sand → clay balls","t":"Wash the sand with an [[create:encased_fan|Encased Fan]] through water; ~25% become clay balls."},
   {"b":"Clay balls → clay → terracotta","t":"Press the balls into clay blocks over a [[create:basin|Basin]], then bulk-blast the clay (fan through fire/lava) into terracotta — no fuel cost."},
   {"b":"Terracotta → red sand → gold","t":"Crush terracotta to red sand, then wash the red sand: ~12% yields gold nuggets. Press nine nuggets into an ingot if you want bars."}]},
  {"note":"Every stage should be joined by belts, and only the front stages need duplicating — build stages 1–3 several times feeding one washer if the line can't keep up. The by-products (flint, dead bush, clay) can all be voided or stored."},
  {"warn":"This is a late-game vanity farm, not an early gold source. Until you've got spare crushing wheels, fans and press capacity to spare, mining or a Nether gold route is faster. Build it because it's magnificent, not because you're short on gold."}]},

"iron":{"title":"Iron (from Gravel)","glyph":"▬","col":"#d8d8d8",
 "sub":"Crush cobble · wash gravel","yields":"Renewable iron, no ore needed",
 "lede":"Create's iron farm makes iron out of nothing but cobblestone. Crush cobble to gravel, wash the gravel, and iron nuggets fall out — a fully renewable metal supply with no ore, no mining and no Nether trip.",
 "body":[
  {"h":"The washing chain"},
  {"p":"The whole farm is a [[minecraft:cobblestone|cobblestone]] generator feeding a crusher feeding a washer. Each stage is cheap; the yield comes from volume, so build the cobble side big."},
  {"steps":[
   {"b":"Crush cobblestone to gravel","t":"A [[create:millstone|Millstone]] or a pair of [[create:crushing_wheel|Crushing Wheels]] fed from a cobble generator. The Millstone is the cheap entry point; wheels move far more."},
   {"b":"Wash the gravel with an [[create:encased_fan|Encased Fan]] through water","t":"Bulk washing gravel gives roughly 12% iron nuggets and 25% flint per item. Keep the nuggets, void or store the flint."},
   {"b":"Press the nuggets into ingots","t":"A [[create:mechanical_press|Mechanical Press]] over a [[create:basin|Basin]] compacts nine nuggets into an iron ingot. A [[create:smart_chute|Smart Chute]] set to filter out flint before the press keeps the line clean."},
   {"b":"Scale by adding fans, not speed","t":"Fan speed doesn't change how fast gravel washes — a fan clears up to 16 gravel every 7.5s. Throughput is set by how many fans and belts you run in parallel, so widen the wash instead of gearing it up."}]},
  {"note":"Fan speed sets how far the wash stream reaches, not its rate: ~1 RPM covers one belt, ~8 two, ~24 three, ~32 four. Line several belts under one wide stream and each adds throughput."},
  {"h":"Doubling actual ore, too"},
  {"p":"If you'd rather process ore you mine, the same machines double it: drop raw ore between [[create:crushing_wheel|Crushing Wheels]] for crushed ore (roughly double the nuggets), wash it for a bonus, then bulk-smelt behind an [[create:encased_fan|Encased Fan]] blowing through lava. That path works for copper, zinc, gold and the modded ores as well."},
  {"warn":"The washer only outputs on chance rolls, so early on it sputters — buffer a stock of gravel before you rely on it. And a lava-fan smelter's [[create:blaze_burner|Blaze Burner]] must stay fed or the line quietly stops."}]},

"melon_pumpkin":{"title":"Melon & Pumpkin","glyph":"❂","col":"#d98b3a",
 "sub":"Drill bar + recombiner","yields":"Whole melons & pumpkins",
 "lede":"Stemmed crops fruit sideways onto the ground, so a low bar of drills sweeping past shears them off. The twist is melons: they harvest as slices, and a Mechanical Crafter downstream glues them back into whole melons for trading.",
 "body":[
  {"h":"The harvesting bar"},
  {"p":"Same moving-bar idea as the linear crop farm, but with drills at fruit height instead of harvesters, because you're breaking melon and pumpkin blocks rather than cutting a crop."},
  {"steps":[
   {"b":"Plant two rows of stems with a walkway between","t":"Slab over the centre water trench so the fruit only ever forms on the tilled strips either side, in a straight line the bar can reach."},
   {"b":"Build a drill bar on [[create:linear_chassis|Linear Chassis]]","t":"[[create:mechanical_drill|Mechanical Drills]] at fruit height, sticky range set to 1 with a Ctrl-[[create:wrench|Wrench]], a chest above to catch the harvest."},
   {"b":"Run it on a [[create:cart_assembler|Cart Assembler]] and [[create:pulse_timer|Pulse Timer]]","t":"Lock Rotation on the assembler, rail out and back, timer set to a few minutes. Same rig as the linear crop farm."},
   {"b":"Hand off with paired [[create:portable_storage_interface|Storage Interfaces]]","t":"Moving one on the bar, fixed one by the rail feeding a belt into the recombiner below."}]},
  {"h":"Recombining slices into whole melons"},
  {"p":"Pumpkins come off whole, but melons come off as slices. To store or trade whole melons, sort the two apart and glue the slices back together."},
  {"steps":[
   {"b":"Split the stream with two [[create:brass_tunnel|Brass Tunnels]]","t":"On parallel belts: one tunnel filtered for melon slices routes them into the crafter, a [[create:filter|List Filter]] rejecting slices lets the pumpkins bypass to storage."},
   {"b":"Feed slices into a 3×3 [[create:mechanical_crafter|Mechanical Crafter]] array","t":"Nine slices make one whole melon. Wrench every crafter's arrow to converge on one output face; a [[create:windmill_bearing|windmill]] on a [[create:rotation_speed_controller|Speed Controller]] is a tidy way to power just the crafter."},
   {"b":"Merge whole melons back with the pumpkins","t":"The crafter's output rejoins the bypass belt into your storage chest or the logistics network."}]},
  {"note":"Balance the planting to the slice math: a melon harvest averages ~5 slices and a whole melon needs 9, so plant about 9 melons for every 5 pumpkins to keep both lines flowing evenly. A farm this size runs to roughly 24 melons and 24 pumpkins an hour."},
  {"warn":"If you don't recombine, melon output piles up as slices and clogs storage fast. Either build the crafter stage or filter slices off to a compost/void — don't let them back up onto the harvest belt."}]},

"tall_crops":{"title":"Sugarcane, Bamboo & Kelp","glyph":"│","col":"#7fae5a",
 "sub":"Piston + saw row","yields":"Cane, bamboo, kelp, paper",
 "lede":"The tall crops don't want a rotating arm. A [[create:mechanical_piston|Mechanical Piston]] dragging a row of saws straight along the planting is simpler and cuts a whole line at once.",
 "body":[
  {"h":"The sliding cutter"},
  {"steps":[
   {"b":"Plant a straight row","t":"Sugarcane on sand beside water, bamboo on any dirt, kelp in a water column. All three grow straight up, which is what makes the sliding cut work."},
   {"b":"Build a [[create:mechanical_piston|Mechanical Piston]] with enough [[create:piston_extension_pole|Extension Poles]] to span the row","t":"The piston needs a pole for every block of travel. Longer rows just need more poles."},
   {"b":"Mount [[create:mechanical_saw|Mechanical Saws]] on the piston head, facing the crop","t":"Set at the height where you want the cut — above the bottom block for sugarcane and bamboo so they regrow, anywhere for kelp."},
   {"b":"Glue the head assembly together and run the piston out and back","t":"A [[create:gearshift|Gearshift]] flipped by a redstone clock reverses it automatically, so it sweeps the row on a loop."},
   {"b":"Catch the drops along the row","t":"A belt or hopper line under the planting carries the harvest to storage."}]},
  {"note":"For a wall of cane or bamboo rather than a single row, a [[create:gantry_carriage|Gantry Carriage]] gives two-axis travel — the same saws sweeping across a whole field instead of one line."},
  {"h":"From cane to paper"},
  {"p":"Sugarcane crushed or pressed becomes paper, and paper is the backbone of the [[create:packager|logistics network]] (every package needs cardboard, which comes from paper). A cane farm feeding a press is often the quiet prerequisite that unblocks the whole factory layer."},
  {"warn":"Kelp harvested wet needs drying before it burns as fuel — run it through a fan smelter first. Bamboo grows fast enough to overwhelm a slow belt, so size the output line for it."}]},

"tree":{"title":"Tree Farm","glyph":"▥","col":"#8a6f1c",
 "sub":"Saw ring on a bearing","yields":"Logs, then planks & more",
 "lede":"The build everyone makes second, because it feeds everything else — and done right, it needs no brass at all. A spinning ring of saws does the chopping.",
 "body":[
  {"h":"The saw carousel"},
  {"steps":[
   {"b":"Run a [[create:water_wheel|Water Wheel]] underground, out of the way","t":"Tuck it into a channel below the trees. A vertical run of [[create:shaft|Shafts]] carries the rotation up to the surface."},
   {"b":"Feed that shaft into a [[create:mechanical_bearing|Mechanical Bearing]] at ground level","t":"Point it up at the structure you're about to build — the bearing spins whatever's glued in front of it."},
   {"b":"Glue a ring of blocks to the bearing, each carrying a [[create:mechanical_saw|Mechanical Saw]] facing outward","t":"As many arms as you have trees to reach. A Saw moving as part of a contraption fells any tree it swings into."},
   {"b":"Glue a chest onto the assembly","t":"Any inventory riding a contraption picks up its own drops automatically — no belt or hopper needed to catch the logs."},
   {"b":"Right-click the bearing to assemble, then power it","t":"It sweeps through the trees around it, felling anything the saws touch and dropping logs straight into the chest riding along."}]},
  {"note":"To empty that chest without walking over, add a [[create:portable_storage_interface|Portable Storage Interface]] to it and place a second on the ground, a block or two off the contraption's path. They connect whenever the moving one swings past, trade items, then let it carry on — no brass, no redstone, no pause."},
  {"note":"Stopping the ring: on Create 6 you can just leave the [[create:mechanical_bearing|Bearing]] reachable and right-click to start/stop it. Otherwise put a [[create:clutch|Clutch]] on the shaft, or set the bearing's movement mode so the structure stays placed when stopped — that keeps the saplings from being knocked out each time it halts."},
  {"h":"Never running dry — the Deployer"},
  {"p":"For a farm that replants itself, add a [[create:deployer|Deployer]] holding saplings just inside each Saw so it plants as the ring passes. The catch is reach: a Saw hits the block right in front of it, but a Deployer reaches the block <i>two</i> away — so back-to-back they miss each other. Stagger them, saws leading and deployers trailing by a row:"},
  {"schem":["  S S S S      <- saws, outer","  C C C C C C  <- chassis arm","    D D D D    <- deployers, one row in"]},
  {"p":"Put a [[create:filter|filter]] or a single sapling in each Deployer's slot; give different Deployers different saplings and one ring farms a mix of tree types at once. A [[create:smart_chute|Smart Chute]] set to keep exactly one stack of saplings in the chest feeds replanting while the surplus flows to storage."},
  {"note":"Yields run roughly 6–10 logs per tree by species (dark oak and cherry the richest), plus saplings, sticks and — from oak — the odd apple. Remember one sapling per spot has to go back in, so never let the sapling buffer hit zero or that column stops regrowing."},
  {"warn":"Saws swinging through a forest will happily cut trees you meant to keep. Fence the farm's reach, or build it somewhere the ring only ever meets trees you planted."}]},
}

# ---------------- HTML ----------------
html = io.StringIO()
W = html.write

W('''<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Cogwork">
<meta name="theme-color" content="#14100d">
<title>The Cogwork Manual</title>
<style>
:root{
 --soot:#14100d;--iron:#1e1813;--iron-hi:#2a221a;
 --brass:#c9a227;--brass-lo:#8a6f1c;--brass-hi:#f0d478;
 --copper:#b5673a;--verdigris:#5a9c88;--andesite:#9a978c;--parchment:#e9dfc7;
 --rivet:rgba(240,212,120,.30);--line:rgba(201,162,39,.24);
 --shadow:0 2px 0 rgba(0,0,0,.5),0 8px 24px rgba(0,0,0,.45);
 --display:"Superclarendon","Bookman Old Style",Rockwell,"Roboto Slab",Georgia,serif;
 --engrave:Copperplate,"Copperplate Gothic Light",Optima,"Gill Sans",serif;
 --body:"Iowan Old Style",Charter,"Palatino Linotype",Georgia,serif;
 --data:"American Typewriter","Courier New",ui-monospace,monospace;
 --r:3px;
}
*{box-sizing:border-box;-webkit-tap-highlight-color:rgba(201,162,39,.15)}
html,body{margin:0;padding:0}
body{background:var(--soot);
 background-image:radial-gradient(120% 70% at 50% -10%,rgba(181,103,58,.16),transparent 60%),
  repeating-linear-gradient(0deg,rgba(255,255,255,.014) 0 1px,transparent 1px 3px);
 color:var(--parchment);font-family:var(--body);font-size:17px;line-height:1.62;
 -webkit-text-size-adjust:100%;padding-bottom:calc(72px + env(safe-area-inset-bottom));overflow-x:hidden}
a{color:var(--verdigris);text-decoration:none;border-bottom:1px dotted rgba(90,156,136,.55)}
a:active{color:var(--brass-hi)}
:focus-visible{outline:2px solid var(--brass);outline-offset:2px}
.topbar{position:sticky;top:0;z-index:50;display:flex;align-items:center;gap:10px;
 padding:calc(8px + env(safe-area-inset-top)) 12px 8px;
 background:linear-gradient(180deg,rgba(20,16,13,.97),rgba(20,16,13,.88));
 backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.iconbtn{flex:0 0 auto;width:38px;height:38px;border-radius:50%;border:1px solid var(--line);
 background:var(--iron-hi);color:var(--brass);font-size:17px;display:grid;place-items:center;cursor:pointer;
 box-shadow:inset 0 1px 0 rgba(240,212,120,.14)}
.iconbtn:active{background:#332818}
.crumb{flex:1;min-width:0;font-family:var(--engrave);font-size:10.5px;letter-spacing:.16em;
 text-transform:uppercase;color:var(--andesite);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.crumb b{color:var(--brass);font-weight:400}
.navbar{position:fixed;left:0;right:0;bottom:0;z-index:60;display:grid;grid-template-columns:repeat(4,1fr);
 background:linear-gradient(180deg,#241c14,#15110d);border-top:2px solid var(--brass-lo);
 padding-bottom:env(safe-area-inset-bottom)}
.navbar button{background:none;border:0;color:var(--andesite);padding:9px 4px 10px;cursor:pointer;
 font-family:var(--engrave);font-size:9px;letter-spacing:.12em;text-transform:uppercase;
 display:flex;flex-direction:column;align-items:center;gap:3px}
.navbar .gl{font-size:19px;line-height:1;color:inherit}
.navbar button[aria-current="true"]{color:var(--brass-hi)}
main{padding:0 18px 26px;max-width:720px;margin:0 auto}
h1,h2,h3{font-family:var(--display);font-weight:400;letter-spacing:-.01em;margin:0}
h1{font-size:31px;line-height:1.1}
h2{font-size:22px;margin:30px 0 10px;color:var(--brass-hi)}
h3{font-size:17.5px;margin:20px 0 6px;color:var(--copper)}
.eyebrow{font-family:var(--engrave);font-size:10px;letter-spacing:.24em;text-transform:uppercase;
 color:var(--andesite);margin:0 0 6px}
p{margin:0 0 12px}.lede{color:#d6cbb2}
.fine{font-size:13.5px;color:var(--andesite);line-height:1.5}
.mono{font-family:var(--data);font-size:14px}
.hero{padding:24px 0 6px;text-align:center}
.hero h1{font-size:34px}
.hero .sub{font-family:var(--engrave);font-size:10px;letter-spacing:.3em;text-transform:uppercase;color:var(--copper);margin-top:8px}
.gearstack{display:flex;justify-content:center;align-items:center;margin-bottom:6px}
@keyframes spinCW{to{transform:rotate(360deg)}}
@keyframes spinCCW{to{transform:rotate(-360deg)}}
.g-cw{transform-origin:50% 50%;animation:spinCW 9s linear infinite}
.g-ccw{transform-origin:50% 50%;animation:spinCCW 4.5s linear infinite}
@media (prefers-reduced-motion:reduce){.g-cw,.g-ccw{animation:none}}
.rule{display:flex;align-items:center;gap:10px;margin:26px 0 4px}
.rule::before,.rule::after{content:"";height:1px;flex:1;background:linear-gradient(90deg,transparent,var(--line),transparent)}
.rule span{font-family:var(--engrave);font-size:10px;letter-spacing:.26em;text-transform:uppercase;color:var(--brass)}
.gauges{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:16px}
.gauge{display:flex;flex-direction:column;align-items:center;gap:8px;padding:14px 6px 12px;cursor:pointer;
 background:linear-gradient(180deg,#2a2118,#1a1510);border:1px solid var(--line);border-radius:var(--r);
 box-shadow:var(--shadow),inset 0 1px 0 rgba(240,212,120,.10);text-align:center}
.gauge:active{transform:translateY(1px)}
.dial{width:52px;height:52px;border-radius:50%;
 background:radial-gradient(circle at 34% 28%,#4a3a1f,#241b11 62%,#15100b);border:2px solid var(--brass-lo);
 box-shadow:inset 0 0 12px rgba(0,0,0,.8),0 0 0 3px rgba(20,16,13,.9),0 0 0 4px rgba(201,162,39,.22);
 display:grid;place-items:center;color:var(--brass-hi);font-size:23px;line-height:1}
.gauge .lbl{font-family:var(--engrave);font-size:9.5px;letter-spacing:.1em;text-transform:uppercase;line-height:1.35}
.tokens{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}
.token{border:1px solid var(--line);border-radius:var(--r);cursor:pointer;
 background:linear-gradient(180deg,#241d15,#191410);padding:12px 5px 10px;
 display:flex;flex-direction:column;align-items:center;gap:7px;text-align:center}
.token:active{background:#2e2417}
.medal{width:42px;height:42px;border-radius:50%;display:grid;place-items:center;font-size:19px;line-height:1;
 background:radial-gradient(circle at 32% 26%,#3d301b,#1d160f);border:1.5px solid currentColor;
 box-shadow:inset 0 0 8px rgba(0,0,0,.7);flex:0 0 auto}
.token .nm{font-family:var(--engrave);font-size:9px;letter-spacing:.06em;text-transform:uppercase;color:var(--parchment);line-height:1.3}
.token .ct{font-family:var(--data);font-size:9px;color:var(--brass-lo)}
.row{display:flex;align-items:center;gap:12px;width:100%;text-align:left;cursor:pointer;
 padding:11px 12px;margin:7px 0;border:1px solid var(--line);border-radius:var(--r);
 background:linear-gradient(180deg,#221b14,#191410);color:var(--parchment);font-family:var(--body);font-size:16px}
.row:active{background:#2c2317}
.row .medal{width:34px;height:34px;font-size:16px}
.row .meta{flex:1;min-width:0}
.row .meta b{display:block;font-weight:400;font-size:16px;line-height:1.25}
.row .meta i{display:block;font-style:normal;font-family:var(--engrave);font-size:8.5px;
 letter-spacing:.14em;text-transform:uppercase;color:var(--andesite);margin-top:2px;
 white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.row .chev{color:var(--brass-lo);font-size:15px}
.recipe{border:1px solid var(--line);border-radius:var(--r);margin:12px 0;overflow:hidden;
 background:linear-gradient(180deg,#221b14,#181310)}
.recipe .station{font-family:var(--engrave);font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;
 color:var(--soot);background:linear-gradient(180deg,var(--brass-hi),var(--brass));
 padding:6px 12px;display:flex;justify-content:space-between;gap:8px;align-items:center}
.recipe .station em{font-style:normal;font-family:var(--data);font-size:9.5px;letter-spacing:0;opacity:.8;text-transform:none}
.recipe ul{list-style:none;margin:0;padding:10px 12px}
.recipe li{display:flex;align-items:baseline;gap:9px;padding:4px 0;border-bottom:1px dotted rgba(154,151,140,.16)}
.recipe li:last-child{border-bottom:0}
.recipe li .qty{font-family:var(--data);font-size:13px;color:var(--brass);min-width:30px;flex:0 0 auto}
.recipe .note{padding:2px 12px 11px;font-size:13px;color:var(--andesite);line-height:1.5}
.recipe .yield{padding:9px 12px;border-top:1px solid var(--line);font-size:14.5px;background:rgba(201,162,39,.05)}
.recipe .yield .qty{font-family:var(--data);color:var(--brass);font-size:13px}
.grid{display:grid;gap:4px;padding:12px;justify-content:center}
.cell{width:38px;height:38px;border:1px solid var(--line);border-radius:2px;background:#100c09;
 display:grid;place-items:center;font-size:16px;color:var(--brass-lo);cursor:pointer}
.cell.on{color:var(--brass-hi);background:#241c12;border-color:var(--brass-lo)}
.cell.empty{opacity:.25;cursor:default}
.note-brass,.note-warn{border-left:3px solid var(--brass);padding:11px 13px;margin:14px 0;
 background:rgba(201,162,39,.07);font-size:15px;line-height:1.55;border-radius:0 var(--r) var(--r) 0}
.note-warn{border-left-color:var(--copper);background:rgba(181,103,58,.09)}
.note-brass b,.note-warn b{color:var(--brass-hi);font-weight:400;font-family:var(--engrave);
 font-size:10px;letter-spacing:.16em;text-transform:uppercase;display:block;margin-bottom:3px}
.note-warn b{color:var(--copper)}
ol.steps{counter-reset:s;list-style:none;padding:0;margin:14px 0}
ol.steps li{counter-increment:s;position:relative;padding:0 0 16px 44px}
ol.steps li::before{content:counter(s);position:absolute;left:0;top:-2px;width:30px;height:30px;border-radius:50%;
 display:grid;place-items:center;font-family:var(--data);font-size:14px;color:var(--brass-hi);
 background:radial-gradient(circle at 34% 28%,#3d301b,#1a140e);border:1.5px solid var(--brass-lo)}
ol.steps li::after{content:"";position:absolute;left:15px;top:30px;bottom:2px;width:1px;
 background:linear-gradient(180deg,var(--line),transparent)}
ol.steps li:last-child::after{display:none}
ol.steps li b{display:block;font-family:var(--display);font-size:16.5px;color:var(--parchment);font-weight:400;margin-bottom:2px}
pre.schem{font-family:var(--data);font-size:12.5px;line-height:1.45;color:var(--brass-hi);background:#100c09;
 border:1px solid var(--line);border-radius:var(--r);padding:12px;overflow-x:auto;margin:12px 0;-webkit-overflow-scrolling:touch}
.searchwrap{position:relative;margin:14px 0 6px}
.searchwrap input{width:100%;padding:13px 14px 13px 40px;font-family:var(--body);font-size:16px;
 color:var(--parchment);background:#100c09;border:1px solid var(--line);border-radius:var(--r)}
.searchwrap input::placeholder{color:#6d685e}
.searchwrap .mag{position:absolute;left:13px;top:50%;transform:translateY(-50%);color:var(--brass-lo)}
details{border:1px solid var(--line);border-radius:var(--r);margin:9px 0;background:#1b1610}
details summary{padding:10px 13px;cursor:pointer;list-style:none;font-family:var(--engrave);
 font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--brass)}
details summary::-webkit-details-marker{display:none}
details summary::after{content:" \\25BE";color:var(--brass-lo)}
details[open] summary::after{content:" \\25B4"}
details .inner{padding:0 13px 12px}
.field{margin:12px 0}
.field label{display:block;font-family:var(--engrave);font-size:9.5px;letter-spacing:.16em;
 text-transform:uppercase;color:var(--andesite);margin-bottom:5px}
.field input{width:100%;padding:11px 12px;font-family:var(--data);font-size:16px;color:var(--parchment);
 background:#100c09;border:1px solid var(--line);border-radius:var(--r)}
.readout{font-family:var(--data);font-size:15px;color:var(--brass-hi);background:#100c09;
 border:1px solid var(--line);border-radius:var(--r);padding:12px;margin-top:12px}
.readout .big{font-size:26px;display:block;line-height:1.2}
.card{padding:16px 15px;margin:12px 0;background:linear-gradient(180deg,var(--iron-hi),var(--iron) 55%,#191410);
 border:1px solid var(--line);border-radius:var(--r);box-shadow:var(--shadow)}
.more{width:100%;padding:12px;margin:10px 0;background:#1b1610;border:1px dashed var(--line);
 border-radius:var(--r);color:var(--brass);font-family:var(--engrave);font-size:10px;
 letter-spacing:.18em;text-transform:uppercase;cursor:pointer}
footer{padding:26px 0 8px;text-align:center;color:#6d685e;font-size:12px;font-family:var(--engrave);
 letter-spacing:.14em;text-transform:uppercase}
</style></head><body>
<div class="topbar">
 <button class="iconbtn" id="btnBack" aria-label="Back">\u2039</button>
 <div class="crumb" id="crumb">The Cogwork Manual</div>
 <button class="iconbtn" id="btnHome" aria-label="Home">\u2302</button>
</div>
<main id="app"></main>
<nav class="navbar">
 <button data-go="#/"><span class="gl">\u2302</span>Home</button>
 <button data-go="#/search"><span class="gl">\u2315</span>Search</button>
 <button data-go="#/mods"><span class="gl">\u26ED</span>Mods</button>
 <button data-go="#/bench"><span class="gl">\u233E</span>Bench</button>
</nav>
<script id="payload" type="application/json">''')
W(payload)
W('</script>\n<script id="wikipayload" type="application/json">')
W(wiki_payload)
W('</script>\n<script>\nconst MODS=')
W(json.dumps(MODS, separators=(',',':')))
W(';\nconst STATIONS=')
W(json.dumps(STATIONS, separators=(',',':')))
W(';\nconst CURATED=')
W(json.dumps(CURATED, separators=(',',':')))
W(';\nconst GUIDES=')
W(json.dumps(GUIDES, separators=(',',':')))
W(';\nconst FARMS=')
W(json.dumps(FARMS, separators=(',',':')))
W(''';

/* ---------- unpack ---------- */
const D=JSON.parse(document.getElementById('payload').textContent);
const S=D.S,T=D.T,R=D.R,NAMES=D.N,TAGX=D.G;
const WIKI=JSON.parse(document.getElementById('wikipayload').textContent);
const modInfo={}; MODS.forEach(m=>modInfo[m[0]]={id:m[0],n:m[1],g:m[2],c:m[3],b:m[4]});

/* indices: which recipes produce / consume each item */
const MAKES={},USES={};
for(let ri=0;ri<R.length;ri++){
  const r=R[ri];
  for(const o of r[1]){ (MAKES[o[0]]||(MAKES[o[0]]=[])).push(ri); }
  const seen=new Set();
  for(const i of r[2]){ if(!seen.has(i[0])){seen.add(i[0]);(USES[i[0]]||(USES[i[0]]=[])).push(ri);} }
  const f=r[4]; if(f&&f.q) for(const st of f.q) for(const ix of st[1]){
    if(!seen.has(ix)){seen.add(ix);(USES[ix]||(USES[ix]=[])).push(ri);} }
}
/* items that belong to each namespace, sorted by name */
const BYNS={};
for(let i=0;i<S.length;i++){
  const s=S[i]; if(s[0]==='#') continue;
  const ns=s.split(':')[0]; (BYNS[ns]||(BYNS[ns]=[])).push(i);
}
for(const ns in BYNS) BYNS[ns].sort((a,b)=>nameOf(a).localeCompare(nameOf(b)));

function nameOf(ix){const s=S[ix];return NAMES[s]||s.split(':')[1].replace(/_/g,' ');}
function esc(s){return String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}

/* ---------- glyphs ---------- */
const GLYPH=[[/cogwheel|gear/,'\\u26ED'],[/shaft|rod/,'\\u2502'],[/casing/,'\\u25A9'],
 [/sheet|plate/,'\\u25AD'],[/ingot/,'\\u25AC'],[/nugget/,'\\u00B7'],[/wheel/,'\\u25CD'],
 [/belt|conveyor|chain/,'\\u26D3'],[/funnel|chute|pipe|tube/,'\\u2502'],[/tank|vault|barrel|crate|box/,'\\u25A3'],
 [/bucket|fluid|water|lava|oil|juice|honey|milk/,'\\u25AF'],[/press|piston/,'\\u21E9'],
 [/drill|pickaxe/,'\\u26CF'],[/saw|blade/,'\\u2702'],[/fan|propeller|turbine/,'\\u273A'],
 [/engine|motor|generator|boiler/,'\\u2318'],[/seed|sapling|crop|plant|flower|berr/,'\\u2766'],
 [/cake|pie|bread|cookie|candy|chocolate|sweet|sugar|jam/,'\\u233E'],
 [/soup|stew|pot|meal|dish|salad/,'\\u2338'],[/meat|beef|pork|chicken|fish/,'\\u2619'],
 [/goggle|lens|optic|glass/,'\\u25C9'],[/wrench|tool|hammer|spanner/,'\\u2692'],
 [/sword|armor|helmet|chestplate|boots|shield/,'\\u26E8'],[/track|rail|bogey|train|carriage/,'\\u26D3'],
 [/package|box|parcel/,'\\u25A4'],[/quartz|crystal|gem|diamond|emerald/,'\\u25C8'],
 [/door|window|fence|stair|slab|panel|block|brick|tile|plank/,'\\u25A6'],
 [/lamp|light|torch|lantern/,'\\u2609'],[/wire|cable|energy|electric|battery/,'\\u26A1'],
 [/mechanism|precision|component|module/,'\\u232C'],[/coin|currency|token/,'\\u25CE'],
 [/schematic|blueprint|book|page/,'\\u2637'],[/dust|powder|flour/,'\\u2059'],
 [/log|wood|bark|stripped/,'\\u25A5']];
const FALLBACK=['\\u25C7','\\u25CB','\\u25B3','\\u25A1','\\u2727','\\u2058','\\u2735','\\u25CC'];
function glyphFor(ix){
  const p=S[ix].split(':')[1]||'';
  for(const [re,g] of GLYPH) if(re.test(p)) return g;
  let h=0; for(let i=0;i<p.length;i++) h=(h*31+p.charCodeAt(i))>>>0;
  return FALLBACK[h%FALLBACK.length];
}
function colFor(ix){
  const ns=S[ix].split(':')[0];
  return (modInfo[ns]&&modInfo[ns].c)||(ns==='minecraft'?'#7f7a70':'#9a978c');
}
function medal(ix,size){
  const st=size?`width:${size}px;height:${size}px;font-size:${Math.round(size*.45)}px;`:'';
  return `<span class="medal" style="color:${colFor(ix)};${st}">${glyphFor(ix)}</span>`;
}
function modName(ns){return (modInfo[ns]&&modInfo[ns].n)||ns.replace(/_/g,' ');}

/* ---------- markup links ---------- */
function md(s){
  return String(s).replace(/\\[\\[([a-z0-9_.]+:[a-z0-9_\\/]+)\\|([^\\]]+)\\]\\]/g,(m,id,label)=>{
    const ix=S.indexOf(id);
    return ix>=0?`<a href="#/i/${ix}">${label}</a>`:label;
  });
}

/* ---------- recipe rendering ---------- */
function stationOf(t){const s=STATIONS[t];if(s)return s;
  const p=t.split(':')[1]||t;return [p.replace(/_/g,' ').replace(/\\b\\w/g,c=>c.toUpperCase()),''];}
function chip(ix,qty){
  return `<li><span class="qty">${qty}\\u00D7</span>`+
   `<span><a href="#/i/${ix}">${esc(nameOf(ix))}</a>`+
   (S[ix][0]==='#'?` <span class="fine">(any of several)</span>`:'')+`</span></li>`;
}
function renderRecipe(ri,focusIx){
  const r=R[ri],[st,hint]=stationOf(T[r[0]]);
  const f=r[4]||{};
  let grid='';
  if(r[3]){
    const [pat,key]=r[3], w=Math.max(...pat.map(x=>x.length));
    grid=`<div class="grid" style="grid-template-columns:repeat(${w},38px)">`+
      pat.map(row=>{
        let cells='';
        for(let c=0;c<w;c++){
          const ch=row[c]||' ';
          if(ch===' '||key[ch]===undefined){cells+=`<div class="cell empty"></div>`;}
          else{const ix=key[ch];
            cells+=`<div class="cell on" data-i="${ix}" title="${esc(nameOf(ix))}">${glyphFor(ix)}</div>`;}
        }
        return cells;
      }).join('')+`</div>`;
  }
  const ins=r[2].map(([ix,q])=>chip(ix,q)).join('');
  const outs=r[1].map(([ix,q,ch])=>{
    const pct=ch==null?'':(ch<=1?` <span class="fine">${Math.round(ch*100)}% chance</span>`
                                :` <span class="fine">weight ${ch}</span>`);
    const strong=(ix===focusIx);
    return `<div><span class="qty">${q>1?q+'\\u00D7':'1\\u00D7'}</span> `+
      (strong?`<b>${esc(nameOf(ix))}</b>`:`<a href="#/i/${ix}">${esc(nameOf(ix))}</a>`)+pct+`</div>`;
  }).join('');
  let notes=[];
  if(hint)notes.push(hint);
  if(f.h)notes.push(f.h==='heated'?'Requires a lit Blaze Burner underneath':
                    f.h==='superheated'?'Requires a superheated Blaze Burner (fed Blaze Cakes)':f.h);
  if(f.l)notes.push(f.l+' loops of the sequence');
  let seq='';
  if(f.q&&f.q.length){
    seq=`<div class="note"><b style="color:var(--brass);font-family:var(--engrave);font-size:9.5px;letter-spacing:.16em;text-transform:uppercase">Sequence</b><ol style="padding-left:18px;margin:6px 0 0">`+
      f.q.map(([ty,ids])=>`<li>${esc((stationOf('create:'+ty))[0])}${ids.length?': ':''}`+
        ids.map(ix=>`<a href="#/i/${ix}">${esc(nameOf(ix))}</a>`).join(', ')+`</li>`).join('')+`</ol></div>`;
  }
  return `<div class="recipe">
    <div class="station"><span>${esc(st)}</span>${f.p?`<em>${(f.p/20).toFixed(0)}s</em>`:''}</div>
    ${grid}
    ${ins?`<ul>${ins}</ul>`:''}
    ${notes.length?`<div class="note">${esc(notes.join(' \\u00B7 '))}</div>`:''}
    ${seq}
    <div class="yield">${outs}</div>
  </div>`;
}

/* ---------- cog svg ---------- */
function cogSVG(r,teeth,cls,col){
  const ri=r*.62,hub=r*.26,pts=[];
  for(let i=0;i<teeth;i++){const a=(i/teeth)*2*Math.PI,s=(2*Math.PI/teeth)/4;
    pts.push([Math.cos(a)*ri,Math.sin(a)*ri],[Math.cos(a+s)*r,Math.sin(a+s)*r],
             [Math.cos(a+s*2)*r,Math.sin(a+s*2)*r],[Math.cos(a+s*3)*ri,Math.sin(a+s*3)*ri]);}
  const d=pts.map((p,i)=>`${i?'L':'M'}${p[0].toFixed(1)},${p[1].toFixed(1)}`).join('')+'Z';
  return `<svg width="${r*2+4}" height="${r*2+4}" viewBox="${-r-2} ${-r-2} ${r*2+4} ${r*2+4}" aria-hidden="true">
   <g class="${cls}"><path d="${d}" fill="none" stroke="${col}" stroke-width="2" stroke-linejoin="round"/>
   <circle r="${hub}" fill="none" stroke="${col}" stroke-width="2"/><circle r="${hub*.35}" fill="${col}"/></g></svg>`;
}

/* ---------- views ---------- */
const app=document.getElementById('app'),crumbEl=document.getElementById('crumb');

function viewHome(){
  crumbEl.innerHTML='<b>The Cogwork Manual</b>';
  const present=MODS.filter(m=>BYNS[m[0]]&&BYNS[m[0]].length);
  return `<div class="hero"><div class="gearstack">
    ${cogSVG(30,12,'g-cw','#c9a227')}<span style="width:0"></span>${cogSVG(19,9,'g-ccw','#b5673a')}</div>
    <p class="eyebrow" style="margin-bottom:2px">All of Create \\u00B7 1.21.1 \\u00B7 NeoForge</p>
    <h1>The Cogwork Manual</h1><p class="sub">A field guide to rotation</p></div>
  <p class="lede" style="text-align:center">Every recipe in your pack, read straight out of the mod jars.
   ${R.length.toLocaleString()} recipes across ${present.length} Create mods.</p>
  <div class="rule"><span>Field Manual</span></div>
  <div class="gauges">
    <button class="gauge" data-go="#/g/basics"><span class="dial">\\u26ED</span><span class="lbl">Get<br>Started</span></button>
    <button class="gauge" data-go="#/g/starter"><span class="dial">\\u27F2</span><span class="lbl">First<br>Steps</span></button>
    <button class="gauge" data-go="#/g/machines"><span class="dial">\\u2692</span><span class="lbl">Starter<br>Machines</span></button>
    <button class="gauge" data-go="#/g/advanced"><span class="dial">\\u2318</span><span class="lbl">Advanced<br>Works</span></button>
    <button class="gauge" data-go="#/g/logistics"><span class="dial">\\u25A4</span><span class="lbl">Logistics<br>Network</span></button>
    <button class="gauge" data-go="#/farms"><span class="dial">\\u2766</span><span class="lbl">Farms &amp;<br>Contraptions</span></button>
  </div>
  <div class="rule"><span>Create Mods</span></div>
  <p class="fine" style="margin-bottom:14px">Tap a mod for its items. Every ingredient links onward.</p>
  <div class="tokens">${present.map(m=>`<button class="token" data-go="#/m/${m[0]}">
    <span class="medal" style="color:${m[3]}">${m[2]}</span>
    <span class="nm">${esc(m[1])}</span><span class="ct">${BYNS[m[0]].length}</span></button>`).join('')}</div>
  <div class="rule"><span>Instruments</span></div>
  <button class="row" data-go="#/bench"><span class="medal" style="color:#e9dfc7">\\u233E</span>
    <span class="meta"><b>Kinetic Bench</b><i>Gear ratios \\u00B7 stress budget</i></span><span class="chev">\\u203A</span></button>
  <button class="row" data-go="#/search"><span class="medal" style="color:#c9a227">\\u2315</span>
    <span class="meta"><b>Search everything</b><i>${S.length.toLocaleString()} items indexed</i></span><span class="chev">\\u203A</span></button>
  <details><summary>Where this data came from</summary><div class="inner fine">
   Recipes, in-game tooltips, Ponder scene text and advancement blurbs are all read directly from the 202 mod jars in your Prism instance \\u2014 the mods' own explanations of what things do, not a summary. Items with no recipe are worldgen, mob drops or creative-only; items with no write-up anywhere just don't have one in the jars.</div></details>
  <footer>Cogwork Manual</footer>`;
}

function viewMods(){
  crumbEl.innerHTML='Manual / <b>Create Mods</b>';
  const present=MODS.filter(m=>BYNS[m[0]]&&BYNS[m[0]].length);
  const other=Object.keys(BYNS).filter(ns=>!modInfo[ns]).sort((a,b)=>BYNS[b].length-BYNS[a].length);
  return `<div style="padding-top:18px"><p class="eyebrow">Index</p><h1>Create Mods</h1>
   <p class="lede" style="margin-top:8px">${present.length} Create-family mods with items in your pack.</p></div>
   <div class="tokens" style="margin-top:16px">${present.map(m=>`<button class="token" data-go="#/m/${m[0]}">
     <span class="medal" style="color:${m[3]}">${m[2]}</span><span class="nm">${esc(m[1])}</span>
     <span class="ct">${BYNS[m[0]].length}</span></button>`).join('')}</div>
   <div class="rule"><span>Also referenced</span></div>
   <p class="fine">Non-Create mods whose items appear inside Create recipes.</p>
   <div class="tokens">${other.slice(0,24).map(ns=>`<button class="token" data-go="#/m/${ns}">
     <span class="medal" style="color:#7f7a70">\\u25C7</span>
     <span class="nm">${esc(modName(ns))}</span><span class="ct">${BYNS[ns].length}</span></button>`).join('')}</div>
   <footer>${Object.keys(BYNS).length} namespaces</footer>`;
}

let modShown=60,modFilter='';
function viewMod(ns){
  const info=modInfo[ns]||{n:modName(ns),g:'\\u25C7',c:'#7f7a70',b:''};
  crumbEl.innerHTML=`Mods / <b>${esc(info.n)}</b>`;
  const all=BYNS[ns]||[];
  return `<div style="padding-top:18px">
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:10px">
      <span class="medal" style="color:${info.c};width:54px;height:54px;font-size:25px">${info.g}</span>
      <div><p class="eyebrow" style="margin:0">${all.length} items</p>
      <h1 style="font-size:25px">${esc(info.n)}</h1></div></div>
    ${info.b?`<p class="lede">${esc(info.b)}</p>`:''}</div>
   <div class="searchwrap"><span class="mag">\\u2315</span>
     <input id="mq" type="search" placeholder="Filter ${esc(info.n)} items\\u2026"
      autocomplete="off" autocorrect="off" spellcheck="false" value="${esc(modFilter)}"></div>
   <div id="modlist"></div><footer>${esc(info.n)}</footer>`;
}
function renderModList(ns){
  const box=document.getElementById('modlist'); if(!box)return;
  const q=modFilter.trim().toLowerCase();
  let list=BYNS[ns]||[];
  if(q) list=list.filter(ix=>nameOf(ix).toLowerCase().includes(q)||S[ix].includes(q));
  const shown=list.slice(0,modShown);
  box.innerHTML=(list.length?shown.map(ix=>rowFor(ix)).join(''):
    `<div class="note-warn"><b>Nothing matches</b>Try a shorter word.</div>`)+
    (list.length>shown.length?`<button class="more" id="moreBtn">Show more \\u00B7 ${list.length-shown.length} left</button>`:'');
  const mb=document.getElementById('moreBtn');
  if(mb)mb.onclick=()=>{modShown+=120;renderModList(ns);};
}
function rowFor(ix){
  const ns=S[ix].split(':')[0];
  const nR=(MAKES[ix]||[]).length;
  return `<button class="row" data-go="#/i/${ix}">${medal(ix,34)}
   <span class="meta"><b>${esc(nameOf(ix))}</b><i>${esc(modName(ns))}${nR?' \\u00B7 '+nR+' recipe'+(nR>1?'s':''):''}</i></span>
   <span class="chev">\\u203A</span></button>`;
}

let itemShownM=6,itemShownU=8;
function ponderText(p){return p.h+'. '+p.t.join(' ');}
function viewItem(ix){
  ix=+ix;
  if(!S[ix])return '<h1>Not found</h1>';
  const id=S[ix],ns=id.split(':')[0],cur=CURATED[id],wiki=WIKI[id]||{};
  crumbEl.innerHTML=`${esc(modName(ns))} / <b>${esc(nameOf(ix))}</b>`;
  const makes=MAKES[ix]||[],uses=USES[ix]||[];
  const tagx=TAGX[id];
  const lede = (cur&&cur.d) ? md(cur.d)
    : wiki.tip&&wiki.tip.s ? wiki.tip.s
    : wiki.pon&&wiki.pon[0] ? ponderText(wiki.pon[0])
    : '';
  const tipBlock = wiki.tip ? `<div class="note-brass"><b>In-game tooltip</b>
     ${wiki.tip.s?`<p style="margin:0 0 8px">${wiki.tip.s}</p>`:''}
     ${(wiki.tip.p||[]).map(([b,c])=>`<p style="margin:0 0 6px">${b}${c?` <span class="fine">\u2014 ${esc(c)}</span>`:''}</p>`).join('')}
    </div>` : '';
  const ponBlock = (wiki.pon&&wiki.pon.length&&!(wiki.pon.length===1&&lede===ponderText(wiki.pon[0]))) ?
    `<div class="rule"><span>From the Ponder</span></div>` +
    wiki.pon.filter(p=>ponderText(p)!==lede).map(p=>
      `<h3 style="color:var(--verdigris);font-size:15px;margin:14px 0 4px">${p.h}</h3>
       ${p.t.map(x=>`<p style="margin:0 0 6px">${x}</p>`).join('')}`).join('') : '';
  const advBlock = wiki.adv ? `<div class="rule"><span>Advancements</span></div>
    ${wiki.adv.map(a=>`<div class="row" style="cursor:default"><span class="medal" style="color:#c9a227">\u2726</span>
      <span class="meta"><b>${a.t}</b>${a.d?`<i style="text-transform:none;font-family:var(--body);font-size:13px;letter-spacing:0">${a.d}</i>`:''}</span></div>`).join('')}` : '';
  return `<div style="padding-top:18px">
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:10px">${medal(ix,54)}
     <div><p class="eyebrow" style="margin:0">${esc(modName(ns))}</p>
     <h1 style="font-size:25px">${esc(nameOf(ix))}</h1></div></div>
    ${lede?`<p class="lede">${lede}</p>`:''}
    <p class="fine mono">${esc(id)}</p></div>
    ${tipBlock}

   ${tagx?`<div class="rule"><span>This tag accepts</span></div>
     <p class="fine">Any of these will satisfy a recipe asking for it.</p>
     ${tagx.map(t=>{const j=S.indexOf(t);return j>=0?rowFor(j):
       `<button class="row" disabled>${'<span class="medal" style="color:#7f7a70">\\u25C7</span>'}
        <span class="meta"><b>${esc(NAMES[t]||t)}</b><i>not used in any recipe here</i></span></button>`;}).join('')}`:''}

   ${makes.length?`<div class="rule"><span>How to make it</span></div>
     ${makes.slice(0,itemShownM).map(ri=>renderRecipe(ri,ix)).join('')}
     ${makes.length>itemShownM?`<button class="more" data-more="m">Show ${makes.length-itemShownM} more recipe${makes.length-itemShownM>1?'s':''}</button>`:''}`
    :(tagx||lede?'':`<div class="note-warn" style="margin-top:18px"><b>No recipe</b>
      Nothing in the pack crafts this. It's worldgen, a mob drop, a creative-only item, or you get it from an
      in-world interaction the recipe files don't describe.</div>`)}

   ${cur&&cur.t&&cur.t.length?`<div class="rule"><span>In practice</span></div>
     <ul style="padding-left:18px">${cur.t.map(t=>`<li style="margin-bottom:8px">${md(t)}</li>`).join('')}</ul>`:''}

   ${uses.length?`<div class="rule"><span>Used to make</span></div>
     ${[...new Set(uses.map(ri=>R[ri][1][0][0]))].slice(0,itemShownU).map(o=>rowFor(o)).join('')}
     ${new Set(uses.map(ri=>R[ri][1][0][0])).size>itemShownU?
       `<button class="more" data-more="u">Show ${new Set(uses.map(ri=>R[ri][1][0][0])).size-itemShownU} more</button>`:''}`:''}

   ${ponBlock}
   ${advBlock}
   <div class="rule"><span>Nearby</span></div>
   <button class="row" data-go="#/m/${ns}">${'<span class="medal" style="color:'+((modInfo[ns]||{}).c||'#7f7a70')+'">'+((modInfo[ns]||{}).g||'\\u25C7')+'</span>'}
     <span class="meta"><b>All ${esc(modName(ns))} items</b><i>Back to the mod index</i></span>
     <span class="chev">\\u203A</span></button>
   <footer>${esc(nameOf(ix))}</footer>`;
}

function renderBody(body){
  return body.map(b=>{
    if(b.h)return `<h2>${md(b.h)}</h2>`;
    if(b.p)return `<p>${md(b.p)}</p>`;
    if(b.note)return `<div class="note-brass"><b>Tip</b>${md(b.note)}</div>`;
    if(b.warn)return `<div class="note-warn"><b>Watch out</b>${md(b.warn)}</div>`;
    if(b.list)return `<ul style="padding-left:18px;margin:8px 0 14px">${b.list.map(x=>`<li style="margin-bottom:6px">${md(x)}</li>`).join('')}</ul>`;
    if(b.schem)return `<pre class="schem">${b.schem.map(esc).join('\\n')}</pre>`;
    if(b.steps)return `<ol class="steps">${b.steps.map(s=>`<li><b>${md(s.b)}</b>${md(s.t)}</li>`).join('')}</ol>`;
    return '';}).join('');
}
function viewGuide(k){
  const g=GUIDES[k]; if(!g)return '<h1>Not found</h1>';
  crumbEl.innerHTML=`Manual / <b>${esc(g.title)}</b>`;
  const body=renderBody(g.body);
  const others=Object.keys(GUIDES).filter(x=>x!==k);
  return `<div style="padding-top:18px"><p class="eyebrow">${esc(g.eyebrow)}</p>
    <h1>${esc(g.title)}</h1><p class="lede" style="margin-top:8px">${md(g.lede)}</p></div>${body}
    <div class="rule"><span>Keep reading</span></div>
    ${others.map(x=>`<button class="row" data-go="#/g/${x}"><span class="medal" style="color:#c9a227">\\u2637</span>
      <span class="meta"><b>${esc(GUIDES[x].title)}</b><i>${esc((GUIDES[x].eyebrow.split('\\u00B7 ')[1]||''))}</i></span>
      <span class="chev">\\u203A</span></button>`).join('')}
    <footer>End of section</footer>`;
}

/* ---------- farms ---------- */
function farmKeys(){return Object.keys(FARMS).sort((a,b)=>FARMS[a].title.localeCompare(FARMS[b].title));}
function farmToken(k){const f=FARMS[k];
  return `<button class="token" data-go="#/f/${k}">
    <span class="medal" style="color:${f.col}">${f.glyph}</span>
    <span class="nm">${esc(f.title)}</span><span class="ct">${esc(f.sub||'')}</span></button>`;
}
function viewFarms(){
  crumbEl.innerHTML='Manual / <b>The Works</b>';
  const keys=farmKeys();
  return `<div style="padding-top:18px"><p class="eyebrow">Field Manual \\u00B7 The Works</p>
    <h1>Farms &amp; Contraptions</h1>
    <p class="lede" style="margin-top:8px">Machines that make things for you. Pick what you want to automate \\u2014 each is a full build, roughly in the order they become worth making.</p></div>
   <div class="tokens" style="margin-top:16px">${keys.map(farmToken).join('')}</div>
   <div class="note-brass" style="margin-top:20px"><b>Growing list</b>
    This catalogue is being filled in over time. Missing the one you want? It's on the way \\u2014 the pattern is always the same: a rotation source, a tool that does the work, and a way to catch what falls out.</div>
   <footer>${keys.length} builds</footer>`;
}
function viewFarm(k){
  const f=FARMS[k]; if(!f)return '<h1>Not found</h1>';
  crumbEl.innerHTML=`The Works / <b>${esc(f.title)}</b>`;
  const body=renderBody(f.body);
  const others=farmKeys().filter(x=>x!==k);
  return `<div style="padding-top:18px">
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:10px">
      <span class="medal" style="color:${f.col};width:54px;height:54px;font-size:25px">${f.glyph}</span>
      <div><p class="eyebrow" style="margin:0">Farms \\u00B7 ${esc(f.sub||'')}</p>
      <h1 style="font-size:25px">${esc(f.title)}</h1></div></div>
    <p class="lede" style="margin-top:4px">${md(f.lede)}</p></div>
    ${f.yields?`<div class="recipe"><div class="station"><span>Yields</span></div>
      <div class="yield">${md(f.yields)}</div></div>`:''}
    ${body}
    <div class="rule"><span>More of The Works</span></div>
    ${others.map(farmToken).join('')?`<div class="tokens">${others.map(farmToken).join('')}</div>`:''}
    <button class="row" data-go="#/farms" style="margin-top:10px"><span class="medal" style="color:#5a9c88">\\u2637</span>
      <span class="meta"><b>All farms &amp; contraptions</b><i>Back to The Works</i></span>
      <span class="chev">\\u203A</span></button>
    <footer>End of build</footer>`;
}

let sq='',sShown=50;
function viewSearch(){
  crumbEl.innerHTML='Manual / <b>Search</b>';
  return `<div style="padding-top:18px"><p class="eyebrow">Index</p><h1>Search</h1></div>
   <div class="searchwrap"><span class="mag">\\u2315</span>
    <input id="q" type="search" placeholder="andesite, press, brass, elevator\\u2026"
     autocomplete="off" autocorrect="off" spellcheck="false" value="${esc(sq)}"></div>
   <div id="results"></div><footer>${S.length.toLocaleString()} items indexed</footer>`;
}
function runSearch(){
  const out=document.getElementById('results'); if(!out)return;
  const q=sq.trim().toLowerCase();
  if(!q){out.innerHTML=`<div class="note-brass" style="margin-top:16px"><b>Try</b>
    A material ("brass"), a machine ("press"), or a whole family ("casing", "cogwheel", "package").</div>`;return;}
  const gh=Object.keys(GUIDES).filter(k=>(GUIDES[k].title+' '+GUIDES[k].lede+JSON.stringify(GUIDES[k].body)).toLowerCase().includes(q));
  const fh=farmKeys().filter(k=>(FARMS[k].title+' '+FARMS[k].sub+' '+FARMS[k].lede+JSON.stringify(FARMS[k].body)).toLowerCase().includes(q));
  const hits=[];
  for(let i=0;i<S.length;i++){
    if(S[i][0]==='#')continue;
    const n=nameOf(i).toLowerCase();
    let score=-1;
    if(n===q)score=0; else if(n.startsWith(q))score=1;
    else if(n.includes(q))score=2; else if(S[i].includes(q))score=3;
    if(score>=0)hits.push([score,n,i]);
  }
  hits.sort((a,b)=>a[0]-b[0]||a[1].localeCompare(b[1]));
  const shown=hits.slice(0,sShown);
  out.innerHTML=
   (gh.length?`<div class="rule"><span>Guides</span></div>`+gh.map(k=>`<button class="row" data-go="#/g/${k}">
     <span class="medal" style="color:#c9a227">\\u2637</span>
     <span class="meta"><b>${esc(GUIDES[k].title)}</b><i>Field manual</i></span><span class="chev">\\u203A</span></button>`).join(''):'')
   +(fh.length?`<div class="rule"><span>Farms</span></div>`+fh.map(k=>`<button class="row" data-go="#/f/${k}">
     <span class="medal" style="color:${FARMS[k].col}">${FARMS[k].glyph}</span>
     <span class="meta"><b>${esc(FARMS[k].title)}</b><i>${esc(FARMS[k].sub||'The Works')}</i></span><span class="chev">\\u203A</span></button>`).join(''):'')
   +(hits.length?`<div class="rule"><span>${hits.length.toLocaleString()} item${hits.length===1?'':'s'}</span></div>`
     +shown.map(h=>rowFor(h[2])).join('')
     +(hits.length>shown.length?`<button class="more" id="moreS">Show more \\u00B7 ${hits.length-shown.length} left</button>`:'')
    :`<div class="note-warn" style="margin-top:16px"><b>Nothing found</b>Try a shorter word.</div>`);
  const b=document.getElementById('moreS'); if(b)b.onclick=()=>{sShown+=100;runSearch();};
}

function viewBench(){
  crumbEl.innerHTML='Manual / <b>Kinetic Bench</b>';
  return `<div style="padding-top:18px"><p class="eyebrow">Instrument</p><h1>Kinetic Bench</h1>
   <p class="lede" style="margin-top:8px">Work out a gear ratio before you build it, and see what a speed change costs.</p></div>
   <div class="card"><p class="eyebrow" style="margin-bottom:10px">Gear ratio</p>
    <div class="field"><label>Source speed (RPM)</label><input id="bSrc" type="number" inputmode="decimal" value="16"></div>
    <div class="field"><label>Small \\u2192 Large steps (each halves)</label><input id="bDown" type="number" inputmode="numeric" value="0"></div>
    <div class="field"><label>Large \\u2192 Small steps (each doubles)</label><input id="bUp" type="number" inputmode="numeric" value="2"></div>
    <div class="readout" id="bOut"></div></div>
   <div class="card"><p class="eyebrow" style="margin-bottom:10px">Stress budget</p>
    <div class="field"><label>Network capacity (SU)</label><input id="sCap" type="number" inputmode="numeric" value="256"></div>
    <div class="field"><label>Currently used (SU)</label><input id="sUse" type="number" inputmode="numeric" value="128"></div>
    <div class="field"><label>Impact of the machine to add</label><input id="sImp" type="number" inputmode="decimal" value="4"></div>
    <div class="field"><label>\\u2026running at (RPM)</label><input id="sRpm" type="number" inputmode="decimal" value="16"></div>
    <div class="readout" id="sOut"></div></div>
   <div class="note-brass"><b>How stress works</b>
    A machine's cost is its impact multiplied by the RPM it runs at \\u2014 which is why gearing a drill up to
    256 RPM is so expensive. Read your real figures off a
    [[create:stressometer|Stressometer]] while wearing [[create:goggles|Goggles]].</div>
   <footer>Kinetic Bench</footer>`;
}
function runBench(){
  const n=id=>{const e=document.getElementById(id);return e?parseFloat(e.value)||0:0;};
  const bo=document.getElementById('bOut');
  if(bo){const src=n('bSrc'),dn=Math.max(0,Math.min(12,n('bDown'))),up=Math.max(0,Math.min(12,n('bUp')));
   const r=src*Math.pow(2,up)/Math.pow(2,dn);
   bo.innerHTML=`<span class="big">${+r.toFixed(2)} RPM</span>ratio ${Math.pow(2,up)}:${Math.pow(2,dn)} from ${src} RPM
    ${r>256?'<div style="color:#b5673a;margin-top:8px">Over the 256 RPM cap \\u2014 the network refuses to run.</div>':''}
    ${r>0&&r<1?'<div style="color:#b5673a;margin-top:8px">Below 1 RPM. Most machines do nothing down here.</div>':''}`;}
  const so=document.getElementById('sOut');
  if(so){const cap=n('sCap'),use=n('sUse'),cost=n('sImp')*n('sRpm'),after=use+cost,bad=after>cap;
   so.innerHTML=`<span class="big" style="${bad?'color:#b5673a':''}">${+cost.toFixed(1)} SU</span>
    network at ${after.toFixed(0)} of ${cap.toFixed(0)} SU (${cap?Math.round(after/cap*100):0}%)
    <div style="margin-top:8px;color:${bad?'#b5673a':'#5a9c88'}">${bad
      ?'Overstressed. Add a source, gear it down, or split the network.'
      :'Fits. '+(cap-after).toFixed(0)+' SU of headroom left.'}</div>`;}
}

/* ---------- router ---------- */
function route(){
  const h=location.hash||'#/', p=h.slice(2).split('/');
  let out;
  if(p[0]==='')out=viewHome();
  else if(p[0]==='g')out=viewGuide(p[1]);
  else if(p[0]==='farms')out=viewFarms();
  else if(p[0]==='f')out=viewFarm(p[1]);
  else if(p[0]==='mods')out=viewMods();
  else if(p[0]==='m'){modShown=60;modFilter='';out=viewMod(p[1]);}
  else if(p[0]==='i'){itemShownM=6;itemShownU=8;out=viewItem(p[1]);}
  else if(p[0]==='search'){sShown=50;out=viewSearch();}
  else if(p[0]==='bench')out=viewBench();
  else out=viewHome();
  app.innerHTML=out; window.scrollTo(0,0);
  const base='#/'+(p[0]||'');
  document.querySelectorAll('.navbar button').forEach(b=>{
    const g=b.dataset.go;
    b.setAttribute('aria-current',String(g===base||(g==='#/'&&h==='#/')||(g==='#/mods'&&p[0]==='m')));});
  if(p[0]==='m'){
    const mq=document.getElementById('mq');
    mq.addEventListener('input',e=>{modFilter=e.target.value;modShown=60;renderModList(p[1]);});
    renderModList(p[1]);
  }
  if(p[0]==='search'){
    const q=document.getElementById('q');
    q.addEventListener('input',e=>{sq=e.target.value;sShown=50;runSearch();});
    runSearch(); if(!sq)setTimeout(()=>q.focus(),80);
  }
  if(p[0]==='bench'){app.addEventListener('input',runBench);runBench();}
  if(p[0]==='i'){
    app.querySelectorAll('[data-more]').forEach(b=>b.onclick=()=>{
      if(b.dataset.more==='m')itemShownM+=12; else itemShownU+=30;
      const scroll=window.scrollY; app.innerHTML=viewItem(p[1]);
      window.scrollTo(0,scroll);
      app.querySelectorAll('[data-more]').forEach(x=>x.onclick=b.onclick);
    });
  }
}
document.addEventListener('click',e=>{
  const cell=e.target.closest('.cell.on');
  if(cell){location.hash='#/i/'+cell.dataset.i;return;}
  const t=e.target.closest('[data-go]');
  if(t){e.preventDefault();location.hash=t.dataset.go;}
});
document.getElementById('btnHome').onclick=()=>location.hash='#/';
document.getElementById('btnBack').onclick=()=>{history.length>1?history.back():location.hash='#/';};
window.addEventListener('hashchange',route);
route();
</script></body></html>''')

out = html.getvalue()
open(args.out,'w').write(out)
print('written: %.2f MB' % (len(out)/1048576))
