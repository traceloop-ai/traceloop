package main

import (
	"fmt"
	"log"

	"github.com/spf13/cobra"
	"github.com/traceloop-ai/traceloop/server"
)

var (
	version = "0.1.0"
	commit  = "dev"
)

func main() {
	rootCmd := &cobra.Command{
		Use:   "traceloop",
		Short: "Production observability for AI agents",
		Long: `Traceloop provides comprehensive observability and monitoring 
for AI agents, offering trace collection, visualization, 
and performance analytics for production AI systems.`,
		Version: fmt.Sprintf("%s (%s)", version, commit),
	}

	rootCmd.AddCommand(serverCmd())
	rootCmd.AddCommand(versionCmd())

	if err := rootCmd.Execute(); err != nil {
		log.Fatal(err)
	}
}

func serverCmd() *cobra.Command {
	var port int
	var host string

	cmd := &cobra.Command{
		Use:   "server",
		Short: "Start the traceloop server",
		Long:  "Start the traceloop server to collect and serve trace data",
		RunE: func(cmd *cobra.Command, args []string) error {
			config := server.Config{
				Host: host,
				Port: port,
			}
			return server.Start(config)
		},
	}

	cmd.Flags().IntVarP(&port, "port", "p", 8080, "Port to run the server on")
	cmd.Flags().StringVar(&host, "host", "localhost", "Host to bind the server to")

	return cmd
}

func versionCmd() *cobra.Command {
	return &cobra.Command{
		Use:   "version",
		Short: "Print version information",
		Run: func(cmd *cobra.Command, args []string) {
			fmt.Printf("traceloop version %s (%s)\n", version, commit)
		},
	}
}
