export const heroes = [
  {
    "id": 1,
    "name": "GAZLOWE",
    "image": "../../assets/heroes_portraits/gazlowe.png",
    "patchNotes": [
      {
        "id": 1,
        "title": "Talent rework",
        "general": [],
        "developerCommentary": "Right now Gazlowe is a mix of a mage and an Auto Attacker where he doesn't shine in both roles. His auto attack build ain't complete enough and the mage build centers on comboing his ultimate. What i want to accomplish here is to make his kit more play-creative while giving a boost to the auto attack build and i want to do that by boosting his roleplay fantasy while increasing the skill ceiling(not the skill floor)",
        "sections": [
          {
            "name": "Level 1",
            "changes": [
              {
                "name": "New: MOLL-E Blingtron 5000 Gift(Active)",
                "texts": [
                  {
                    "text": "Activate to put a Mailbox that will give a random item after 30 seconds the items disappears after 60 if not picked and after 2 minutes if not used. Any hero can get the items (Cooldown 20 seconds):",
                    "subtexts": [
                      "Invisibility Field - Grants invisibility for 10 seconds.",
                      "Hyperspeed Accelerators - Grants speed by 20% for 3 seconds.",
                      "Grounded Plasma Shield - Grants 200 shield for 3 seconds."
                    ]
                  }
                ],
                "developerCommentary": "This is made thinking on improve gazlowe utility as a 4-man hero rather than a solo laner granting her more of gadget power to his side."
              },
              {
                name: 'One Man Wrecking Crew',
                texts: [
                  {
                    text: 'removed',
                  },
                ],
                developerCommentary: 'As a competitor to Big Game Hunter this talent serves less purposes for the auto attack build as putting more turrets it\'s both more beneficial and cooler for Gazlowe than just hitting harder',
              },
              {
                name: 'Big Game Hunter',
                texts: [
                  {
                    text: 'Additional functionality: Destroying a turret with Reduce, Reuse, Recycle gives Gazlowe 15% movespeed for 2 seconds',
                  },
                ],
                developerCommentary: 'The auto attack is a build more focused on solo laners and it requires Gazlowe to hit heroes. The problem with that relies on Gazlowe\'s methods to reach enemies or crowd control them. His bomb is hard to hit, and the movement speed on basic attacks comes only on level 16, with no mobility, he has hard times going for the enemies. The only reliable source for him to for the auto attacks safely and early is the slow he gets when hitting with Master Blaster talent. So the objective here is to bring up the tools for him to go for this auto attack build faster by making a synergy with the extra scrap and making it a more high skill ceiling talent.',
              },
            ],
          },
          {
            name: 'Level 4',
            changes: [
              {
                name: 'EZ-PZ Dimensional Ripper',
                texts: [
                  {
                    text: 'Changed functionality: Destroying a turret with Reduce, Reuse, Recycle reduces enemy heroes nearby that turret damage by 20% and increase allied heros armor by 10 for 4 seconds, Gazlowe will receive a shield that absorbs 100 damage for each hero affected for 2.5 seconds',
                  },
                ],
                developerCommentary: 'EZ-PZ Dimensional Ripper and Rock It Sock It kinda fight for the same spot of utility, one being more turret focused and the other being a more eazy to pick talent but it kinda undermines build variety with 2 talents covering the same topic. For that instance both talents also works in a way too simple that >IN MY OPINION< could be more valued in a higher skill ceiling talent that also doesn\'t too complex. The objective here is to make that talent viable both as a 4-man and a solo laner while showing that skill expression that i talked about as the enemy hero damage reduction would work better in 1v1\'s and the armor would work better when close to your team.',
              },
              {
                name: 'Rock It Sock It',
                texts: [
                  {
                    text: 'Removed',
                  },
                ],
                developerCommentary: 'I mixed this talent with EZ-PZ Dimensional Ripper',
              },
              {
                name: 'New: Mekgineer\'s Mount 5000',
                texts: [
                  {
                    text: 'Gazlowe mount let another mount together on a mining cart installed by Gazlowe, the allied hero will mount instantly to the gazlowe cart without reseting his own mount cooldown',
                    subtexts: [
                      'Nitro boosts(Active): Activate to make Gazlowe becomes unstopabble for 5 seconds and can\'t be unmounted by damage while mounted and increases his mount speed to 150%, loses the effect if Gazlowe dismounts ( Cooldown 30 seconds )',
                    ],
                  },
                ],
                developerCommentary: 'Gazlowe is a tinker but isn\'t building much.Roleplay fantasy is a must and clip moments of Gazlowe saving teammates would be damn popular, i am only uncertain if should be added an effect that prevents Gazlowe being unmounted if he takes damage lower than 2% of his health as that talent could alredy be fairly strong on rotations',
              },
              {
                name: 'Hyperfocus Coils',
                texts: [
                  {
                    text: 'Changed functionality: Heroes hit with Deth Lazor are affected by zapped for 3 seconds dealing 40 damage per second to enemy heros close to them. Hitting the same enemy hero with Deth Lazor and Xplodium Charge within 3 seconds on a enemy hero makes Gazlowe zaps all his Rock-It! Turret to deal damage to the enemies. Gazlowe is healed 100% of all zapped damage',
                  },
                ],
                developerCommentary: 'Hyperfocus Coils original effects serves his purpose for the mage talent build BUT it\'s not only about serving the purpose that makes HOTS talents cool but also how they affect your gameplay, straight number buffs are not necessarily game changers and I FELT that on this. The changes here are made to make the original purpose stay..damage+healing on the Deth Lazor but also adding more interactions and effects that would make the player play potential increase',
              },
            ],
          },
          {
            name: 'Level 7',
            changes: [
              {
                name: 'Cardboard Assassin(active)',
                texts: [
                  {
                    text: 'Activate to place a Cardboard Assassin decoy unit that have 1000 health and act as a heroic unit for 10 seconds.',
                  },
                  {
                    text: 'If you hit Cardboard Assassin with Deth Lazor it becomes zapped and deals enemy heros 40 damage per second and taunts enemy heros for 0.5 second, after 3 seconds it explodes.(Cooldown 10 seconds)',
                  },
                  {
                    text: 'Passive: Deth Lazor cooldown is reduced by 2 seconds',
                  },
                ],
                developerCommentary: 'CardBoard Assassin is made with the intention to increase the skill expression of gazlowe while also mainting the roleplay of builder fantasy',
              },
              {
                name: 'Overload',
                texts: [
                  {
                    text: 'Moved to level 13',
                  },
                ],
                developerCommentary: 'With the new Cardboard Assassin Overload would start to be undervalued',
              },
            ],
          },
          {
            name: 'Level 10',
            changes: [
              {
                name: 'Robo-Goblin',
                texts: [
                  {
                    text: 'Additional functionality:  Rock-It! Turrets now explode dealing 135 damage to enemies when they are destroyed',
                  },
                  {
                    text: "additional functionality: Increase max scrap limit by 6 and increase scrap regeneration speed by 50%"
                  },
                ],
                developerCommentary: 'Robo-Goblin ain\'t a big game changer compared to Grav-o-Bomb for your build to be picked and not effective as much BUT with the additional power the talents i created/modified i believe that making it have a increased synergy with Rock-it! Turret would make it A GAME CHANGER for some builds.',
              },
            ],
          },
          {
            name: 'Level 13',
            changes: [
              {
                name: 'Overcharged Capacitors',
                texts: [
                  {
                    text: 'Removed',
                  },
                ],
                developerCommentary: 'Increase the ability damage is part of the Grav-O-Bomb 3000 effect and further increasing it\'s spell power on a counter intuitive way of auto attacking ain\'t the best solution for my gameplay vision. I understand that this talent was made for mage players to value more their turrets but there are another ways that i would prefer to',
              },
              {
                name: 'Overload',
                texts: [
                  {
                    text: 'Changed functionality: Deth Lazor can now be recast during its channeling up to three times, each recast will increase the channel time in 0.65 the area in 100% of it\'s base area and the damage by 75% of the base damage',
                  },
                  {
                  text: 'moved from level 7'
                  },
                ],
                developerCommentary: 'Overload on level 13 is an option to replace Overcharged Capacitors while also making Gazlowe more prone to creative plays. The ideia of increasing Deth Lazor casting better suit what i envision of player control instead of the original effect of non-stop reseting.',
              },
              {
                name: 'Positive Reinforcement',
                texts: [
                  {
                    text: 'Additional functionality: Dealing Basic Attack adamage extends the duration of Rock-it! Turrets by 0.75 seconds',
                  },
                ],
                developerCommentary: 'I always felt that this talent effects belongs to an AA build as it rewards more the Gazlowe players that risk themselves more for the basic attacks',
              },
            ],
          },
          {
            name: 'Level 16',
            changes: [
              {
                name: 'Overklock',
                texts: [
                  {
                    text: 'No changes',
                  },
                ],
                developerCommentary: 'I just want to note that the movement speed you get from Big Game Hunter needs to stack with that talent granting an effective 30% movespeed bonus if used correctly',
              },
              {
                name: 'Firin\' Mah Lazorz',
                texts: [
                  {
                    text: 'Changed functionality:  Rock-It! Turrets every 5 seconds will charge a lazor making it next shoot deal 125 damage',
                  },
                  {
                    text: '(Active) L-A-Z-O-R: The next time you cast a Deth Lazor will make all your Rock-it! Turrets shoot a lazor(30 seconds cooldown)',
                  },
                ],
                developerCommentary: 'Changing Firin\' Mah Lazors to be more consistent and reliable',
              },
            ],
          },
          {
            name: 'Level 20',
            changes: [
              {
                name: 'Mecha lord',
                texts: [
                  {
                    text: 'Changed functionality: Basic Attacks increase Gazlowe\'s Armor by 10 for 10 seconds, up to a maximum of 30.',
                  },
                  {
                    text:  'Goblin missile(active) - Deplay a homing missile to seek the targeted enemy unit. The missile gains speed over time, dealing 300 damage and stunning for 1.5 second when it impacts the target. Enemy units can destroy the missile before it reaches its target. ( cooldown 60 seconds )',
                    subtexts: ['Reference Homing missile - https://www.dota2.com/hero/gyrocopter']
                  },
                ],
                developerCommentary: 'Mecha Lord doesn\'t encourages basic attacks build enough neither it can compete with It\'s Raining Scrap on the build, so, you don\'t need to try to compete with it. Gazlowe as a tinkerer should have a happy time as a builder. For instance i don\'t even mine it being a copy cat of Gyrocopter homing missile because it suits SO WELL gazlowe',
              },
            ],
          },
        ],
      },
    ],
  },
];