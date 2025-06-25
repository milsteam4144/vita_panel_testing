// tests/unit/fortune-system.test.js
const { getRandomFortune, displayStartupFortune, FORTUNES } = require('../../claude-conduit-fortunes');

describe('Fortune System', () => {
  describe('getRandomFortune()', () => {
    test('should return a valid fortune object', () => {
      const fortune = getRandomFortune();
      
      expect(fortune).toHaveProperty('claude-conduit');
      expect(typeof fortune['claude-conduit']).toBe('object');
    });

    test('should return different fortunes on multiple calls', () => {
      const fortunes = new Set();
      
      // Get 20 fortunes to test randomness
      for (let i = 0; i < 20; i++) {
        fortunes.add(JSON.stringify(getRandomFortune()));
      }
      
      // Should have some variety (at least 5 different fortunes)
      expect(fortunes.size).toBeGreaterThan(5);
    });

    test('should always return fortunes from the FORTUNES array', () => {
      for (let i = 0; i < 10; i++) {
        const fortune = getRandomFortune();
        expect(FORTUNES).toContainEqual(fortune);
      }
    });
  });

  describe('FORTUNES array', () => {
    test('should contain valid JSON fortune objects', () => {
      FORTUNES.forEach((fortune, index) => {
        expect(fortune).toHaveProperty('claude-conduit');
        expect(typeof fortune['claude-conduit']).toBe('object');
        
        // Each fortune should have at least one property
        const fortuneContent = fortune['claude-conduit'];
        expect(Object.keys(fortuneContent).length).toBeGreaterThan(0);
      });
    });

    test('should include VIBE fortunes', () => {
      const vibeFortunesCount = FORTUNES.filter(fortune => 
        JSON.stringify(fortune).includes('VIBE')
      ).length;
      
      expect(vibeFortunesCount).toBeGreaterThan(0);
    });

    test('should include FLOW methodology fortunes', () => {
      const flowFortunesCount = FORTUNES.filter(fortune => 
        JSON.stringify(fortune).toLowerCase().includes('flow')
      ).length;
      
      expect(flowFortunesCount).toBeGreaterThan(0);
    });

    test('should include embedded commands', () => {
      const embeddedCommandFortunes = FORTUNES.filter(fortune => {
        const fortuneStr = JSON.stringify(fortune).toLowerCase();
        return fortuneStr.includes('notice') || 
               fortuneStr.includes('feel') || 
               fortuneStr.includes('watch') ||
               fortuneStr.includes('experience') ||
               fortuneStr.includes('remember');
      });
      
      expect(embeddedCommandFortunes.length).toBeGreaterThan(5);
    });

    test('should include teacherbot references', () => {
      const teacherbotFortunes = FORTUNES.filter(fortune => 
        JSON.stringify(fortune).includes('teacherbot')
      );
      
      expect(teacherbotFortunes.length).toBeGreaterThan(0);
    });

    test('should include special user requests', () => {
      const userRequestedPhrases = [
        "You're already doing it",
        "Who's a good girl?",
        "Thanks, Dad",
        "teacherbot.help has a posse"
      ];

      userRequestedPhrases.forEach(phrase => {
        const found = FORTUNES.some(fortune => 
          JSON.stringify(fortune).includes(phrase)
        );
        expect(found).toBeTruthy();
      });
    });

    test('should include Live2D metadata for future integration', () => {
      const live2dMetadataFortunes = FORTUNES.filter(fortune => {
        const fortuneStr = JSON.stringify(fortune);
        return fortuneStr.includes('tail_wagging') || 
               fortuneStr.includes('confidence') ||
               fortuneStr.includes('encouragement');
      });
      
      expect(live2dMetadataFortunes.length).toBeGreaterThan(0);
    });
  });

  describe('displayStartupFortune()', () => {
    let consoleSpy;

    beforeEach(() => {
      consoleSpy = jest.spyOn(console, 'log').mockImplementation();
    });

    afterEach(() => {
      consoleSpy.mockRestore();
    });

    test('should display formatted fortune on startup', () => {
      displayStartupFortune();
      
      // Should have called console.log multiple times
      expect(consoleSpy).toHaveBeenCalled();
      
      // Check that it includes the startup fortune header
      const output = consoleSpy.mock.calls.map(call => call[0]).join('\n');
      expect(output).toContain('🔮 claude-conduit startup fortune:');
      expect(output).toContain('='.repeat(70));
    });

    test('should display valid JSON in output', () => {
      displayStartupFortune();
      
      const output = consoleSpy.mock.calls.map(call => call[0]).join('\n');
      
      // Extract JSON portion (between the = lines)
      const jsonMatch = output.match(/\{[\s\S]*\}/);
      expect(jsonMatch).toBeTruthy();
      
      // Should be valid JSON
      expect(() => JSON.parse(jsonMatch[0])).not.toThrow();
    });
  });

  describe('Fortune Categories', () => {
    test('should include SOLID principles', () => {
      const solidFortunes = FORTUNES.filter(fortune => {
        const content = fortune['claude-conduit'];
        return content.solid || JSON.stringify(content).includes('SOLID');
      });
      
      expect(solidFortunes.length).toBeGreaterThanOrEqual(5); // S, O, L, I, D
    });

    test('should include Agile principles', () => {
      const agileFortunes = FORTUNES.filter(fortune => 
        JSON.stringify(fortune).toLowerCase().includes('agile')
      );
      
      expect(agileFortunes.length).toBeGreaterThan(0);
    });

    test('should include developer reality checks', () => {
      const realityFortunes = FORTUNES.filter(fortune => {
        const fortuneStr = JSON.stringify(fortune).toLowerCase();
        return fortuneStr.includes('rubber duck') ||
               fortuneStr.includes('stack overflow') ||
               fortuneStr.includes('works on my machine') ||
               fortuneStr.includes('coffee');
      });
      
      expect(realityFortunes.length).toBeGreaterThan(3);
    });
  });

  describe('Educational Patterns', () => {
    test('should use consistent embedded command patterns', () => {
      const embeddedCommands = ['notice', 'feel', 'watch', 'experience', 'remember'];
      
      embeddedCommands.forEach(command => {
        const commandFortunes = FORTUNES.filter(fortune => 
          JSON.stringify(fortune).toLowerCase().includes(command)
        );
        
        expect(commandFortunes.length).toBeGreaterThan(0);
      });
    });

    test('should include confidence-building language', () => {
      const confidenceWords = ['confidence', 'building', 'growing', 'improving', 'deserved'];
      
      confidenceWords.forEach(word => {
        const wordFortunes = FORTUNES.filter(fortune => 
          JSON.stringify(fortune).toLowerCase().includes(word)
        );
        
        expect(wordFortunes.length).toBeGreaterThan(0);
      });
    });
  });
});

// Test helper for manual fortune inspection
describe('Fortune Inspector (Manual)', () => {
  test.skip('should display all VIBE fortunes for review', () => {
    const vibeFortunesCount = FORTUNES.filter(fortune => {
      const hasVibe = JSON.stringify(fortune).includes('VIBE') || 
                     JSON.stringify(fortune).includes('vibe');
      if (hasVibe) {
        console.log(JSON.stringify(fortune, null, 2));
      }
      return hasVibe;
    }).length;
    
    console.log(`\nTotal VIBE fortunes: ${vibeFortunesCount}`);
  });

  test.skip('should display sample fortune output for verification', () => {
    console.log('\n=== Sample Fortune Outputs ===');
    for (let i = 0; i < 5; i++) {
      console.log(JSON.stringify(getRandomFortune(), null, 2));
      console.log('---');
    }
  });
});