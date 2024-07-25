import MyAxios from '@/plugins/myAxios.ts';


export const getTeamList = async (val='', status=0) => {
    return await MyAxios.get("/team/list", {
        params: {
            searchText: val,
            status,
        }
    })
}

export const formatISO8601 = (strTime: string) => {
    return strTime.replace('T', ' ')
}