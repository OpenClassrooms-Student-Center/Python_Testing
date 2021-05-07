class ErrorDisplayer {
    constructor(parent_container) {
        this.parent_container = parent_container
        this.div_container = document.createElement("div")
        this.div_container.className = "errors-container"
        this.list_container = document.createElement("ul")
        this.div_container.append(this.list_container)
        this.parent_container.append(this.div_container)
        this.error_list = new Map()

        this.add = function (error_key, error_value) {
            if (this.list_container == null)
                this.create_error_container()
            if (!this.error_list.has(error_key)) {
                this.error_list.set(error_key, error_value)
                let error_node = document.createElement("li")
                error_node.innerHTML = error_value
                error_node.className = "error"
                this.list_container.append(error_node)
            }
        }

        this.clear = function () {
            if (this.list_container == null)
                return
            let error_nodes = document.getElementsByClassName("error")
            while (error_nodes.length > 0) {
                error_nodes[0].parentElement.removeChild(error_nodes[0])
            }
            this.error_list = new Map()
        }
    }
}
