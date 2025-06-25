// claude-conduit/server.js
// VIBE-powered bridge connecting Claude Code to MCP servers

const express = require('express');
const fs = require('fs');
const path = require('path');
const os = require('os');
const { displayStartupFortune, getRandomFortune } = require('./claude-conduit-fortunes');

class ClaudeConduit {
  constructor() {
    this.clients = new Map();
    this.app = express();
    this.startTime = Date.now();
    this.version = '1.0.0';
    this.setupMiddleware();
    this.setupRoutes();
  }

  setupMiddleware() {
    // JSON parsing
    this.app.use(express.json({ limit: '10mb' }));
    
    // CORS for local development
    this.app.use((req, res, next) => {
      res.header('Access-Control-Allow-Origin', '*');
      res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
      res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
      
      if (req.method === 'OPTIONS') {
        res.sendStatus(200);
      } else {
        next();
      }
    });

    // Request logging
    this.app.use((req, res, next) => {
      console.log(`${new Date().toISOString()} ${req.method} ${req.path}`);
      next();
    });
  }

  setupRoutes() {
    // Health check endpoint
    this.app.get('/health', (req, res) => {
      const uptime = Math.floor((Date.now() - this.startTime) / 1000);
      
      res.json({
        status: 'ok',
        servers: Array.from(this.clients.keys()),
        uptime: uptime,
        version: this.version,
        environment: {
          node_version: process.version,
          platform: os.platform(),
          arch: os.arch()
        }
      });
    });

    // List all available tools across MCP servers
    this.app.get('/tools', async (req, res) => {
      try {
        const tools = {};
        
        for (const [serverName, client] of this.clients) {
          try {
            // Note: This is pseudo-code for MCP client integration
            // Actual implementation would use MCP SDK methods
            tools[serverName] = await this.getServerTools(client);
          } catch (error) {
            console.error(`Error getting tools from ${serverName}:`, error.message);
            tools[serverName] = { error: error.message };
          }
        }
        
        res.json(tools);
      } catch (error) {
        res.status(500).json({ 
          error: 'Failed to retrieve tools',
          message: error.message 
        });
      }
    });

    // Execute a tool on a specific MCP server
    this.app.post('/execute/:server/:tool', async (req, res) => {
      try {
        const { server, tool } = req.params;
        const client = this.clients.get(server);
        
        if (!client) {
          return res.status(404).json({ 
            error: `Server '${server}' not found`,
            available_servers: Array.from(this.clients.keys())
          });
        }

        // Note: This is pseudo-code for MCP tool execution
        // Actual implementation would use MCP SDK methods
        const result = await this.executeServerTool(client, tool, req.body);
        
        res.json({
          success: true,
          server: server,
          tool: tool,
          result: result,
          timestamp: new Date().toISOString()
        });
        
      } catch (error) {
        console.error(`Error executing ${req.params.server}/${req.params.tool}:`, error);
        res.status(500).json({ 
          error: 'Tool execution failed',
          message: error.message,
          server: req.params.server,
          tool: req.params.tool
        });
      }
    });

    // VIBE fortune endpoint
    this.app.get('/fortune', (req, res) => {
      try {
        const fortune = getRandomFortune();
        res.json({
          ...fortune,
          timestamp: new Date().toISOString(),
          server: 'claude-conduit',
          version: this.version
        });
      } catch (error) {
        res.status(500).json({ 
          error: 'Fortune generation failed',
          message: error.message 
        });
      }
    });

    // Server information endpoint
    this.app.get('/info', (req, res) => {
      res.json({
        name: 'claude-conduit',
        version: this.version,
        description: 'VIBE-powered bridge connecting Claude Code to MCP servers',
        uptime: Math.floor((Date.now() - this.startTime) / 1000),
        connected_servers: Array.from(this.clients.keys()),
        endpoints: [
          'GET /health - Service health check',
          'GET /tools - List available MCP tools',
          'POST /execute/{server}/{tool} - Execute MCP tool',
          'GET /fortune - Get VIBE fortune',
          'GET /info - This endpoint'
        ],
        vibe: getRandomFortune()
      });
    });

    // Root endpoint with welcome message
    this.app.get('/', (req, res) => {
      res.json({
        message: 'claude-conduit: VIBE-powered MCP bridge',
        tagline: 'teacherbot.help has a posse',
        status: 'ready',
        version: this.version,
        fortune: getRandomFortune(),
        next_steps: [
          'GET /health - Check service status',
          'GET /tools - See available MCP tools',
          'GET /fortune - Get encouraging VIBE fortune'
        ]
      });
    });
  }

  // Mock MCP client methods (to be replaced with actual MCP SDK integration)
  async getServerTools(client) {
    // This would use actual MCP SDK methods
    return [
      {
        name: 'example_tool',
        description: 'Example tool for testing',
        input_schema: {
          type: 'object',
          properties: {
            message: { type: 'string' }
          }
        }
      }
    ];
  }

  async executeServerTool(client, toolName, params) {
    // This would use actual MCP SDK methods
    return {
      tool: toolName,
      params: params,
      result: 'Mock execution result - MCP integration pending',
      timestamp: new Date().toISOString()
    };
  }

  async initializeMCPClients() {
    console.log('🔗 Initializing MCP client connections...');
    
    try {
      // Load MCP configuration
      const configPath = process.env.MCP_CONFIG_PATH || 
                        path.join(os.homedir(), '.config', 'claude', 'claude_desktop_config.json');
      
      if (!fs.existsSync(configPath)) {
        console.log(`⚠️  MCP config not found at ${configPath}`);
        console.log('📝 Running in mock mode for development');
        
        // Add mock clients for development
        this.clients.set('mock-server', { type: 'mock', connected: true });
        return;
      }

      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      const mcpServers = config.mcpServers || {};

      for (const [serverName, serverConfig] of Object.entries(mcpServers)) {
        try {
          console.log(`🔌 Connecting to ${serverName}...`);
          
          // Note: Actual MCP client initialization would happen here
          // For now, we're creating mock clients
          const mockClient = {
            name: serverName,
            config: serverConfig,
            connected: true,
            type: 'mock'
          };
          
          this.clients.set(serverName, mockClient);
          console.log(`✅ Connected to ${serverName}`);
          
        } catch (error) {
          console.error(`❌ Failed to connect to ${serverName}:`, error.message);
        }
      }
      
      console.log(`🎯 Initialized ${this.clients.size} MCP client connections`);
      
    } catch (error) {
      console.error('❌ Failed to initialize MCP clients:', error.message);
      console.log('📝 Running in mock mode');
    }
  }

  async start(port = null) {
    // Display VIBE fortune on startup
    displayStartupFortune();
    
    console.log('🌉 Starting claude-conduit bridge server...');
    
    // Initialize MCP client connections
    await this.initializeMCPClients();
    
    // Start HTTP server
    const serverPort = port || process.env.CONDUIT_PORT || 3001;
    const serverHost = process.env.CONDUIT_HOST || 'localhost';
    
    this.app.listen(serverPort, serverHost, () => {
      console.log(`🚀 claude-conduit running on http://${serverHost}:${serverPort}`);
      console.log(`💡 Ready to bridge Claude Code with ${this.clients.size} MCP servers!`);
      console.log(`🔮 VIBE system active - fortune endpoint available at /fortune`);
      console.log(`📊 Health monitoring at /health`);
      console.log('');
      console.log('🎯 Available endpoints:');
      console.log(`   GET  http://${serverHost}:${serverPort}/health`);
      console.log(`   GET  http://${serverHost}:${serverPort}/tools`);
      console.log(`   POST http://${serverHost}:${serverPort}/execute/{server}/{tool}`);
      console.log(`   GET  http://${serverHost}:${serverPort}/fortune`);
      console.log('');
    });
  }

  async shutdown() {
    console.log('🛑 Shutting down claude-conduit...');
    
    // Close MCP client connections
    for (const [serverName, client] of this.clients) {
      try {
        // Note: Actual MCP client cleanup would happen here
        console.log(`🔌 Disconnecting from ${serverName}...`);
      } catch (error) {
        console.error(`❌ Error disconnecting from ${serverName}:`, error.message);
      }
    }
    
    console.log('👋 claude-conduit shutdown complete');
    process.exit(0);
  }
}

// Handle graceful shutdown
process.on('SIGINT', async () => {
  console.log('\n🛑 Received SIGINT, shutting down gracefully...');
  if (global.claudeConduit) {
    await global.claudeConduit.shutdown();
  } else {
    process.exit(0);
  }
});

process.on('SIGTERM', async () => {
  console.log('\n🛑 Received SIGTERM, shutting down gracefully...');
  if (global.claudeConduit) {
    await global.claudeConduit.shutdown();
  } else {
    process.exit(0);
  }
});

// Start the server if this file is run directly
if (require.main === module) {
  const conduit = new ClaudeConduit();
  global.claudeConduit = conduit;
  
  const port = process.argv[2] || process.env.CONDUIT_PORT || 3001;
  conduit.start(port).catch(error => {
    console.error('❌ Failed to start claude-conduit:', error);
    process.exit(1);
  });
}

module.exports = ClaudeConduit;