import MyAxios from '@/plugins/myAxios.ts';


export const getCurrentUser = async () => {
    return await MyAxios.get('user/current')
}

export const getMyTeam = async (teamType: string) => {
    return await MyAxios.get(`/team/list/${teamType}`, {
        params: {
            searchText: ''
        }
    })
}

export const getTotalTags = async () => {
    return await MyAxios.get('/user/totalTags')
}