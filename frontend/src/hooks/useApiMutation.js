import { useMutation } from '@tanstack/react-query'
import api from '../services/api'

export default function useApiMutation(url) {
  return useMutation({ mutationFn: async (payload) => (await api.post(url, payload)).data.data })
}
