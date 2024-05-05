package function

import (
	"fmt"

	faasflow "github.com/faasflow/lib/openfaas"
)

// Define provide definition of the workflow
func Define(flow *faasflow.Workflow, context *faasflow.Context) (err error) {

	dag := flow.Dag()
	dag.Node("n1").Apply("social-network-compose-post")
	dag.Node("n2").Apply("social-network-read-social-graph")
	dag.Node("n3").Apply("social-network-store-post").Modify(func(data []byte) ([]byte, error) {
		return []byte(fmt.Sprintf("Function returned \"%s\"", string(data))), nil
	})
	dag.Node("n4").Apply("social-network-write-home-timeline").Modify(func(data []byte) ([]byte, error) {
		return []byte(fmt.Sprintf("Function returned \"%s\"", string(data))), nil
	})
	dag.Edge("n1", "n2")
	dag.Edge("n1", "n3")
	dag.Edge("n2", "n4")

	// flow.SyncNode().
	// Apply("social-network-compose-post").
	// Apply("social-network-read-user-timeline").
	// Modify(func(data []byte) ([]byte, error) {
	// 	return []byte(fmt.Sprintf("Function returned \"%s\"", string(data))), nil
	// })
	return
}

// OverrideStateStore provides the override of the default StateStore
func OverrideStateStore() (faasflow.StateStore, error) {
	// NOTE: By default FaaS-Flow use consul as a state-store,
	//       This can be overridden with other synchronous KV store (e.g. ETCD)
	return nil, nil
}

// OverrideDataStore provides the override of the default DataStore
func OverrideDataStore() (faasflow.DataStore, error) {
	// NOTE: By default FaaS-Flow use minio as a data-store,
	//       This can be overridden with other synchronous KV store
	return nil, nil
}
