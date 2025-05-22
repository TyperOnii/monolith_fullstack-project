import { WithRedux } from "./providers/withRedux"
import { WithRouter } from "./providers/withRouter"

function App() {

  return (
    <WithRedux>
      <WithRouter/>
    </WithRedux>
  )
}

export default App
